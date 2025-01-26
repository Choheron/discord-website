from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from users.utils import getSpotifyUser

from .models import (
  Album,
  Review,
)

import logging
from dotenv import load_dotenv
import os
import json
import datetime
import pytz

# Declare logging
logger = logging.getLogger('django')

# Determine runtime enviornment
APP_ENV = os.getenv('APP_ENV') or 'DEV'
load_dotenv(".env.production" if APP_ENV=="PROD" else ".env.local")


## =========================================================================================================================================================================================
## REVIEW METHODS
## =========================================================================================================================================================================================

###
# Submit a new review of an album by a user.
###
def submitReview(request: HttpRequest):
  logger.info("submitReview called...")
  # Make sure request is a post request
  if(request.method != "POST"):
    logger.warning("submitReview called with a non-POST method, returning 405.")
    res = HttpResponse("Method not allowed")
    res.status_code = 405
    return res
  # Get data from request
  reqBody = json.loads(request.body)
  # Get user from database
  userObj = getSpotifyUser(request.session.get('discord_id'))
  # Get Album from the database
  albumObj = Album.objects.get(spotify_id=reqBody['album_id'])
  # Check if a review already exists for this user
  try:
    reviewObj = Review.objects.get(album=albumObj, user=userObj)
    reviewObj.score = float(reqBody['score'])
    reviewObj.review_text = reqBody['comment']
    reviewObj.first_listen = reqBody['first_listen']
    # Save/Update Object
    reviewObj.save()
  except Review.DoesNotExist:
    # Declare new Review object
    newReview = Review(
      album=albumObj,
      user=userObj,
      score=float(reqBody['score']),
      review_text=reqBody['comment'],
      first_listen=reqBody['first_listen'],
      aotd_date=datetime.datetime.now(tz=pytz.timezone('America/Chicago')).strftime('%Y-%m-%d'),
    )
    # Save new Review data
    newReview.save()
  return HttpResponse(200)


###
# Get All Reviews for a specific album.
###
def getReviewsForAlbum(request: HttpRequest, album_spotify_id: str):
  logger.info("getReviewsForAlbum called...")
  # Make sure request is a get request
  if(request.method != "GET"):
    logger.warning("getReviewsForAlbum called with a non-GET method, returning 405.")
    res = HttpResponse("Method not allowed")
    res.status_code = 405
    return res
  # Get Album from the database
  try:
    albumObj = Album.objects.get(spotify_id=album_spotify_id)
  except Album.DoesNotExist:
    out = {}
    out['review_list'] = []
    print(f'Album {album_spotify_id} not found...')
    return JsonResponse(out)
  # Get all reivews for album
  try:
    reviewsObj = Review.objects.filter(album=albumObj)
  except Review.DoesNotExist:
    out = {}
    out['review_list'] = []
    print(f'No reviews found for album {album_spotify_id}...')
    return JsonResponse(out)
  # Declare outlist and populate
  outList = []
  for review in reviewsObj:
    outObj = {}
    outObj['user_id'] = review.user.discord_id
    outObj['album_id'] = review.album.spotify_id
    outObj['score'] = review.score
    outObj['comment'] = review.review_text
    outObj['review_date'] = review.review_date.strftime("%m/%d/%Y, %H:%M:%S")
    outObj['last_upated'] = review.last_updated.strftime("%m/%d/%Y, %H:%M:%S")
    outObj['first_listen'] = review.first_listen
    # Append to list
    outList.append(outObj)
  # Return list of reviews
  return JsonResponse({"review_list": outList})


###
# Get USER Reviews for a specific album.
###
def getUserReviewForAlbum(request: HttpRequest, album_spotify_id: str):
  logger.info("getUserReviewForAlbum called...")
  # Make sure request is a get request
  if(request.method != "GET"):
    logger.warning("getUserReviewForAlbum called with a non-GET method, returning 405.")
    res = HttpResponse("Method not allowed")
    res.status_code = 405
    return res
  # Get Album from the database
  try: 
    albumObj = Album.objects.get(spotify_id=album_spotify_id)
  except ObjectDoesNotExist:
    return JsonResponse({"review": None})
  # Get reivew for album
  try: 
    review = Review.objects.get(album=albumObj, user=getSpotifyUser(request.session.get('discord_id')))
  except ObjectDoesNotExist:
    return JsonResponse({"review": None})
  # Declare out object and populate
  outObj = {}
  outObj['user_id'] = review.user.discord_id
  outObj['album_id'] = review.album.spotify_id
  outObj['score'] = review.score
  outObj['comment'] = review.review_text
  outObj['review_date'] = review.review_date.strftime("%m/%d/%Y, %H:%M:%S")
  outObj['last_upated'] = review.last_updated.strftime("%m/%d/%Y, %H:%M:%S")
  outObj['first_listen'] = review.first_listen
  # Return user review
  return JsonResponse({"review": outObj})

###
# Get Review stats for all users.
# TODO: Track streaks of reviews to see which user has been maintaining the streak
###
def getAllUserReviewStats(request: HttpRequest):
  logger.info("getAllUserReviewStats called...")
  # Make sure request is a get request
  if(request.method != "GET"):
    logger.warning("getAllUserReviewStats called with a non-GET method, returning 405.")
    res = HttpResponse("Method not allowed")
    res.status_code = 405
    return res
  # Get all user reviews
  all_reviews = Review.objects.all()
  # Declare reviewData object and populate
  reviewData = {}
  totalReviews = 0
  for review in all_reviews:
    # Increment total review count
    totalReviews += 1
    # If user has not appeared before, create new object for user
    if(review.user.discord_id not in reviewData.keys()):
      reviewData[review.user.discord_id] = {
        "discord_id": review.user.discord_id, # This is the same as the key, just for ease of reference 
        "total_reviews": 0, 
        "review_score_sum": 0,
        "average_review_score": -1, # This will be calculated at the end
        "lowest_score_given": -1,
        "lowest_score_album": None,
        "lowest_score_date": None,
        "highest_score_given": -1,
        "highest_score_album": None,
        "highest_score_date": None,
        }
    # Update review data for user based on current review
    reviewData[review.user.discord_id]['total_reviews'] += 1
    reviewData[review.user.discord_id]['review_score_sum'] += review.score
    if((reviewData[review.user.discord_id]['lowest_score_given'] == -1) or (reviewData[review.user.discord_id]['lowest_score_given'] > review.score)):
      reviewData[review.user.discord_id]['lowest_score_given'] = review.score
      reviewData[review.user.discord_id]['lowest_score_album'] = review.album.spotify_id
      reviewData[review.user.discord_id]['lowest_score_date'] = review.review_date.strftime("%m/%d/%Y, %H:%M:%S")
    if((reviewData[review.user.discord_id]['highest_score_given'] == -1) or (reviewData[review.user.discord_id]['highest_score_given'] <= review.score)):
      reviewData[review.user.discord_id]['highest_score_given'] = review.score
      reviewData[review.user.discord_id]['highest_score_album'] = review.album.spotify_id
      reviewData[review.user.discord_id]['highest_score_date'] = review.review_date.strftime("%m/%d/%Y, %H:%M:%S")
  # Calcualte averages 
  for userReviewData in reviewData.keys():
    reviewData[userReviewData]['average_review_score'] = reviewData[userReviewData]['review_score_sum']/reviewData[userReviewData]['total_reviews']
  # Convert user reviews object to list
  outList = []
  for user in reviewData:
    outList.append(reviewData[user])
  # Return data 
  return JsonResponse({'total_reviews': totalReviews, 'review_data': outList})