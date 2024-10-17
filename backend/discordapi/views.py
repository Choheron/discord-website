from django.http import HttpRequest, HttpResponse, JsonResponse

from backend.utils import (
  postToDiscordWebhook,
)

from users.utils import (
  doesUserExist,
  createUserFromDiscordJSON,
)

from .utils import (
  isDiscordTokenExpired, 
  refreshDiscordToken, 
  storeDiscordTokenInSession,
  checkPreviousAuthorization,
)

import datetime
import logging
import requests
from dotenv import load_dotenv
import os
import json

# Declare logging
logger = logging.getLogger('django')

# Determine runtime enviornment
APP_ENV = os.getenv('APP_ENV') or 'DEV'

load_dotenv(".env.production" if APP_ENV=="PROD" else ".env.local")


###
# Exchange discord auth code for discord api token (part of the login flow)
###
def getDiscordToken(request: HttpRequest):
  logger.info("getDiscordToken called...")
  # Make sure request is a post request
  if(request.method != "POST"):
    logger.warning("getDiscordToken called with a non-POST method, returning 405.")
    res = HttpResponse("Method not allowed")
    res.status_code = 405
    return res
  # Body data
  reqBody = json.loads(request.body)
  # Retrieve code from request
  discordCode = reqBody['code']
  discordRedirectURI = reqBody['redirect_uri']
  # Prep request data and headers to discord api
  reqHeaders = { 
    'Content-Type': 'application/x-www-form-urlencoded',
  }
  reqData = {
    'grant_type': 'authorization_code',
    'code': discordCode,
    'redirect_uri': discordRedirectURI,
    'client_id': os.getenv('DISCORD_CLIENT_ID'),
    'client_secret': os.getenv('DISCORD_CLIENT_SECRET')
  }
  # Make request to discord api
  logger.info("Making request to discord api...")
  discordRes = requests.post(f"{os.getenv('DISCORD_API_ENDPOINT')}/oauth2/token", headers=reqHeaders, data=reqData, auth=(os.getenv('DISCORD_CLIENT_ID'), os.getenv('DISCORD_CLIENT_SECRET')))
  if(discordRes.status_code != 200):
    print("Error in request:\n" + str(discordRes.json()))
    discordRes.raise_for_status()
  # Convert response to Json
  logger.info("Discord api returned, converting to json...")
  discordResJSON = discordRes.json()
  # Store discord data in session data
  storeDiscordTokenInSession(request, discordResJSON)
  # Retrieving discord data to create a user account
  reqHeaders = { 
    'Authorization': f"{request.session['discord_token_type']} {request.session['discord_access_token']}"
  }
  # Send Request to API
  logger.info("Making request to discord api...")
  try:
    discordRes = requests.get(f"{os.getenv('DISCORD_API_ENDPOINT')}/users/@me", headers=reqHeaders)
    if(discordRes.status_code != 200):
      print("Error in request:\n" + str(discordRes.json()))
      discordRes.raise_for_status()
  except:
    return HttpResponse(status=500)
  # Convert response to Json
  discordResJSON = discordRes.json()
  # Store discord ID in session for user data retrieval
  request.session['discord_id'] = discordResJSON['id']
  # Check if user's data exists as a user in the database
  if(not(doesUserExist(discordResJSON['id']))):
    createUserFromDiscordJSON(discordResJSON)
  # Write success message
  messageOut = { 'message': "Success" }
  # Return Code
  logger.info("Returning HTTP 200 Response...")
  return HttpResponse(content=messageOut, content_type='text/json', status=200)


###
# Retrieve basic info about the user and create a user instance
###
def getDiscordUserData(request: HttpRequest):
  logger.info("getDiscordUserData called...")
  logger.info("Cookies in request: " + str(request.COOKIES))
  # Make sure request is a get request
  if(request.method != "GET"):
    logger.warning("getDiscordUserData called with a non-GET method, returning 405.")
    res = HttpResponse("Method not allowed")
    res.status_code = 405
    return res
  # Ensure user is logged in
  if(isDiscordTokenExpired(request)):
    refreshDiscordToken(request)
  # Prep request data and headers to discord api
  reqHeaders = { 
    'Authorization': f"{request.session['discord_token_type']} {request.session['discord_access_token']}"
  }
  # Send Request to API
  logger.info("Making request to discord api...")
  try:
    discordRes = requests.get(f"{os.getenv('DISCORD_API_ENDPOINT')}/users/@me", headers=reqHeaders)
    if(discordRes.status_code != 200):
      print("Error in request:\n" + str(discordRes.json()))
      discordRes.raise_for_status()
  except:
    return HttpResponse(status=500)
  # Convert response to Json
  discordResJSON = discordRes.json()
  # Store discord ID in session for user data retrieval
  request.session['discord_id'] = discordResJSON['id']
  # Check if user's data exists as a user in the database
  if(not(doesUserExist(discordResJSON['id']))):
    createUserFromDiscordJSON(discordResJSON)
  # Return JsonResponse containing user data
  return JsonResponse(discordResJSON)


###
# Validate that the user is a member of the discord server (TODO: Improve this flow, make it dynamic)
###
def validateServerMember(request: HttpRequest):
  # Make sure request is a get request
  if(request.method != "GET"):
    logger.warning("validateServerMember called with a non-GET method, returning 405.")
    res = HttpResponse("Method not allowed")
    res.status_code = 405
    return res
  # Ensure user is logged in
  if(isDiscordTokenExpired(request)):
    refreshDiscordToken(request)
  # Prep headers to discord api
  reqHeaders = { 
    'Authorization': f"{request.session['discord_token_type']} {request.session['discord_access_token']}"
  }
  # Send Request to API
  logger.info("Making request to discord api for server member validation...")
  try:
    discordRes = requests.get(f"{os.getenv('DISCORD_API_ENDPOINT')}/users/@me/guilds", headers=reqHeaders)
    if(discordRes.status_code != 200):
      print("Error in request:\n" + str(discordRes.json()))
      discordRes.raise_for_status()
  except:
    return HttpResponse(status=500)
  # Convert response to List
  discordResList = discordRes.json()
  # Loop through servers and check if member of correct server
  logger.info("Checking if user is in server...")
  member = False
  for server in discordResList:
    if(server['id'] == os.getenv('CORD_SERVER_ID')):
      logger.info("User is in server!")
      member = True
      break
  # Return JsonResponse containing true or false in body
  logger.info("Returning member status...")
  out = {}
  out['member'] = member
  return JsonResponse(out)


###
# Validate that the user has previously approved login
###
def checkIfPrevAuth(request: HttpRequest):
  logger.info("checkIfPrevAuth called...")
  # Make sure request is a get request
  if(request.method != "GET"):
    logger.warning("checkIfPrevAuth called with a non-GET method, returning 405.")
    res = HttpResponse("Method not allowed")
    res.status_code = 405
    return res
  # Check if session is still valid
  validSession = (request.session.get_expiry_age() != 0)
  logger.info(f"Valid Session After Expiry Check: {validSession}")
  # Check if user sessionid token is valid
  logger.info("Ensuring sessionid is valid...")
  # Set output var if session exists
  if(validSession):
    validSession = checkPreviousAuthorization(request)
  # Ensure user is logged in
  if(validSession and isDiscordTokenExpired(request)):
    refreshDiscordToken(request)
  # 
  # Return JsonResponse containing true or false in body
  logger.info(f"Returning prevAuth status of: {validSession}...")
  out = {}
  out['valid'] = validSession
  return JsonResponse(out)


###
# Revoke discord token and clear session data for user
###
def revokeDiscordToken(request: HttpRequest):
  logger.info("revokeDiscordToken called...")
  # Make sure request is a get request
  if(request.method != "GET"):
    logger.warning("revokeDiscordToken called with a non-GET method, returning 405.")
    res = HttpResponse("Method not allowed")
    res.status_code = 405
    return res
  # Ensure user is logged in
  if(isDiscordTokenExpired(request)):
    refreshDiscordToken(request)
  # Prep request data and headers to discord api
  reqHeaders = { 
    'Content-Type': 'application/x-www-form-urlencoded',
  }
  reqData = {
    'client_id': os.getenv('DISCORD_CLIENT_ID'),
    'client_secret': os.getenv('DISCORD_CLIENT_SECRET'),
    'token': request.session['discord_access_token']
  }
  # Make API request to discord to revoke user token
  logger.info("Making token revoke request to discord api...")
  try:
    discordRes = requests.post(f"{os.getenv('DISCORD_API_ENDPOINT')}/oauth2/token/revoke", headers=reqHeaders, data=reqData)
    if(discordRes.status_code != 200):
      print("Error in request:\n" + str(discordRes.json()))
      discordRes.raise_for_status()
  except:
    return HttpResponse(status=500)
  # Clear session data
  logger.info("Flushing session...")
  request.session.flush()
  request.session.modified = True
  # Return JsonResponse containing true or false in body
  logger.info("Returning revoked status...")
  out = {}
  out['status'] = True
  return JsonResponse(out) 