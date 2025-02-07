from django.contrib import admin
from django.urls import path

from . import views_aotd
from . import views_review
from . import views_album
from . import views_user
from . import views_oauth

urlpatterns = [
  ## ============================================================================================================
  ## OAuth Views
  ## ============================================================================================================
  path('token', views_oauth.doSpotifyTokenSwap),
  path('connected', views_oauth.isSpotifyConnected),
  ## ============================================================================================================
  ## User Views
  ## ============================================================================================================
  path('getSpotifyData', views_user.getSpotifyData),
  path('getSpotifyUsersObj', views_user.getSpotifyUsersObj),
  path('getSpotifyUserCount', views_user.getSpotifyUserCount),
  path('getTopItems/<str:item_type>/<str:time_range>/<str:limit>/<str:offset>', views_user.getTopItems),
  path('spotifySearch/<str:item_type>/<str:query>/<str:limit>/<str:offset>', views_user.spotifySearch),
  ## ============================================================================================================
  ## Album Views
  ## ============================================================================================================
  path('checkIfAlbumAlreadyExists/<str:album_spotify_id>', views_album.checkIfAlbumAlreadyExists),
  path('submitAlbum', views_album.submitAlbum),
  path('getAlbum/<str:album_spotify_id>', views_album.getAlbum),
  path('getAllAlbums', views_album.getAllAlbums),
  path('getLastXAlbums/<int:count>', views_album.getLastXAlbums),
  # Below URL has three variations (for different URL params)
  path('getAlbumAvgRating/<str:album_spotify_id>/<str:rounded>/<str:date>', views_album.getAlbumAvgRating),
  path('getAlbumAvgRating/<str:album_spotify_id>/<str:rounded>', views_album.getAlbumAvgRating),
  path('getAlbumAvgRating/<str:album_spotify_id>', views_album.getAlbumAvgRating),
  # Below URL has two variations (one for lack of URL Param)
  path('checkIfUserCanSubmit/<str:date>', views_album.checkIfUserCanSubmit),
  path('checkIfUserCanSubmit', views_album.checkIfUserCanSubmit),
  # Statistics Endpoints
  path('getAlbumsStats', views_album.getAlbumsStats),
  path('getLowestHighestAlbumStats', views_album.getLowestHighestAlbumStats), 
  ## ============================================================================================================
  ## Review Views
  ## ============================================================================================================
  path('submitReview', views_review.submitReview),
  # Below URL has two variations, one in which a date is provided and one where it isnt
  path('getReviewsForAlbum/<str:album_spotify_id>/<str:date>', views_review.getReviewsForAlbum),
  path('getReviewsForAlbum/<str:album_spotify_id>', views_review.getReviewsForAlbum),
  path('getUserReviewForAlbum/<str:album_spotify_id>', views_review.getUserReviewForAlbum),
  path('getAllUserReviewStats', views_review.getAllUserReviewStats),
  path('getSimilarReviewsForRatings', views_review.getSimilarReviewsForRatings),
  ## ============================================================================================================
  ## Album Of the Day Views
  ## ============================================================================================================
  # Below URL has two variations (one for lack of URL Param)
  path('getAlbumOfDay/<str:date>', views_aotd.getAlbumOfDay),
  path('getAlbumOfDay', views_aotd.getAlbumOfDay),
  # Command to be called by cronjob to set the album of the day
  path('setAlbumOfDay', views_aotd.setAlbumOfDay),
  # ADMIN Command to be called by admin for special occasion album of the days
  path('setAlbumOfDayADMIN/<str:date>/<str:album_spotify_id>', views_aotd.setAlbumOfDayADMIN),
  # Return dates in which the passed in album was aotd
  path('getAotdDates/<str:album_spotify_id>', views_aotd.getAotdDates),
]
