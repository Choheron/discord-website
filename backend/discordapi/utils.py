from django.http import HttpRequest

import requests
import datetime 
import os
import json
import logging

# Declare logging
logger = logging.getLogger('django')


def storeDiscordTokenInSession(request: HttpRequest, discordResponseJSON: json):
  logger.info("Attempting to store discord token data in session object...")
  # Store discord data in session data
  request.session["discord_access_token"] = discordResponseJSON['access_token']
  request.session["discord_token_type"] = discordResponseJSON['token_type']
  # Calculate Expiry time then store as string
  expiryTime = datetime.datetime.now() + datetime.timedelta(seconds=discordResponseJSON['expires_in'])
  request.session["discord_expiry_date"] = expiryTime.strftime("%d-%m-%Y %H:%M:%S")
  request.session["discord_refresh_token"] = discordResponseJSON['refresh_token']
  request.session["discord_scope"] = discordResponseJSON['scope']
  logger.info("Discord token data stored in session object!")
  # Return True
  return True


def isDiscordTokenExpired(request: HttpRequest):
  logger.info("Checking if discord token is expired...")
  # Get current time
  curTime = datetime.datetime.now()
  # Get session Expiry time
  tokenExpireTime = datetime.datetime.strptime(request.session['discord_expiry_date'], "%d-%m-%Y %H:%M:%S")
  # Check if request session's discord token is out of date
  if(curTime > tokenExpireTime):
    logger.info("Token IS expired...")
    return True
  # Return false if not expired
  return False


def refreshDiscordToken(request: HttpRequest):
  logger.info("Refreshing Discord Token...")
  # Retrieve session data
  refreshToken = request.session['discord_refresh_token']
  # Prep request data and headers to discord api
  reqHeaders = { 'Content-Type': 'application/x-www-form-urlencoded' }
  reqData = {
     'grant_type': 'refresh_token',
     'refresh_token': refreshToken
   }
  # Make request to discord api
  discordRes = requests.post(f"{os.getenv('DISCORD_API_ENDPOINT')}/oauth2/token", headers=reqHeaders, data=reqData, auth=(os.getenv('DISCORD_CLIENT_ID'), os.getenv('DISCORD_CLIENT_SECRET')))
  if(discordRes.status_code != 200):
    logger.error("Error in request:\n" + discordRes.reason)
    logger.info("More Info: \n" + json.dumps(discordRes.json()))
    discordRes.raise_for_status()
  # Convert response to Json
  discordResJSON = discordRes.json()
  # Store discord data in session data
  storeDiscordTokenInSession(request, discordResJSON)
  # Return True if Successful
  return True


def checkPreviousAuthorization(request: HttpRequest):
  # Check if session is stored in data
  logger.info("Checking if sessionid exists...")
  return 'discord_access_token' in request.session

