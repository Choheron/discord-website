from django.db import models
import logging
from django.forms.models import model_to_dict

from users.models import User

logger = logging.getLogger(__name__)

# Model for spotify data that corresponds to a user
class SpotifyUserData(models.Model):
  # Foriegn key of a user object, primary key, required
  user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    primary_key=True,
  )
  # Spotify Data
  country = models.CharField(max_length=2)
  display_name = models.CharField(
    max_length=150,
    null=True,
  )
  email = models.EmailField(max_length=256)
  spotify_url = models.CharField(max_length=256)
  follower_count = models.IntegerField(default=0)
  user_endpoint = models.CharField(max_length=512)
  spotify_id = models.CharField(max_length=256)
  user_pfp_url = models.CharField(max_length=512, null=True)
  user_pfp_height = models.IntegerField(null=True)
  user_pfp_width = models.IntegerField(null=True)
  membership_type = models.CharField(max_length=256)
  # Automatic Fields
  creation_timestamp = models.DateTimeField(auto_now_add=True)
  # Fields for authentication and login
  access_token = models.CharField(null=True, max_length=512)
  token_type = models.CharField(null=True, max_length=30)
  token_scope = models.CharField(null=True, max_length=512)
  token_expiry_date = models.DateTimeField(null=True)
  refresh_token = models.CharField(null=True, max_length=512)
  # Fields for top songs
  top_track_long_term = models.TextField(null=True)
  # Flag for if their albums are currently blocked
  selection_blocked_flag = models.BooleanField(default=False)

  # toString Method
  def __str__(self):
    return "Spotify:" + self.display_name
  

# Model for an album that has been submitted for album of the day
class Album(models.Model):
    spotify_id = models.CharField(max_length=256, unique=True)  # Spotify Album ID
    title = models.CharField(max_length=256)
    artist = models.CharField(max_length=256)
    artist_url = models.CharField(default="", max_length=512)
    cover_url = models.CharField(max_length=512)
    spotify_url = models.CharField(default="", max_length=512) # Url to access album from spotify
    submitted_by = models.ForeignKey(
      User, 
      on_delete=models.SET_NULL,  # Keep the album, set submitted_by to NULL
      null=True,
      blank=True
    )
    user_comment = models.TextField(null=True, blank=True)  # User's comment on the album
    submission_date = models.DateTimeField(auto_now_add=True) 
    raw_data = models.JSONField(null=True) # JSON field to store all data returned from the frontend

    def subDateToCalString(self):
      return self.submission_date.strftime('%Y-%m-%d')

    # Custom delete function to log the user action
    def delete(self, deleter=None, reason=None, *args, **kwargs):
      # Log the action before actually deleting
      from users.models import UserAction  # Import inside to avoid circular import

      # If deleter is not provided, log critical log and do not delete album
      if( deleter == None):
        logger.critical(f"ATTEMPTED DELETE OF ALBUM (ID: {self.spotify_id}) WITH NO USER PASSED IN! KEEPING ALBUM: {self.title}")
        return
      # Create user action log
      UserAction.objects.create(
        user=deleter, 
        action_type="DELETE",
        entity_type="ALBUM",
        entity_id=self.id,
        details={"reason": reason, "deleted_album": self.title, "album_raw_data": model_to_dict(self) }
      )
      # Call Django's default delete method
      super().delete(*args, **kwargs)


    def __str__(self):
      return f"{self.title} by {self.artist}"


# Model for an album of the day
class DailyAlbum(models.Model):
    album = models.OneToOneField(Album, on_delete=models.CASCADE)
    date = models.DateField(unique=True)
    manual = models.BooleanField(default=False)

    def dateToCalString(self):
      return self.date.strftime('%Y-%m-%d')

    def __str__(self):
      return f"Album for {self.date}: {self.album}"


# Model for a User's review of an album.
class Review(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()  # Score out of 10
    review_text = models.TextField(null=True, blank=True)
    review_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)  # Track the latest update
    first_listen = models.BooleanField(default=None, null=True) # Is this review a result of a first listen?
    aotd_date = models.DateField(null=False) # Attach each review to the aotd date in which it was provided
    # Add review versioning for display
    version = models.IntegerField(default=1)

    class Meta:
        unique_together = ('album', 'user')  # Prevent duplicate reviews for the same user and album

    def save(self, *args, **kwargs):
      from users.models import UserAction
      # Create a history record before updating the review
      if self.pk:  # Only if this is an update, not a new review
        # Create review history object
        history = ReviewHistory.objects.create(
          review=self,
          score=self.score,
          review_text=self.review_text,
          review_date=self.review_date,
          first_listen=self.first_listen,
          aotd_date=self.aotd_date,
          version=self.version
        )
        # Create UserAction for review update
        UserAction.objects.create(
          user=self.user, 
          action_type="UPDATE",
          entity_type="REVIEW",
          entity_id=self.pk,
          details={"old_review_score": self.score, "old_review_text": self.review_text, "reviewhistory_pk": history.pk}
        )
      super().save(*args, **kwargs)

    def __str__(self):
      return f"Review by {self.user.username} for {self.album.title}"


# Model for a User's older review of an album.
class ReviewHistory(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="history")
    score = models.IntegerField()
    review_text = models.TextField(null=True, blank=True)
    review_date = models.DateTimeField()  # Original date of the review
    first_listen = models.BooleanField(default=None, null=True) # Is this review a result of a first listen?
    aotd_date = models.DateField(null=False) # Attach each review to the aotd date in which it was provided
    # Add review versioning for display
    version = models.IntegerField(default=1)

    recorded_at = models.DateTimeField(auto_now_add=True)  # When the history record was created

    def __str__(self):
      return f"History for {self.review} at {self.recorded_at}"
