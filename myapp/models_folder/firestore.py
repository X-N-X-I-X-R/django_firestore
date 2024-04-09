from django import apps
import firebase_admin
from firebase_admin import credentials, firestore
from myapp.models_folder.models import Post, Comment, Like, Follow, UserProfile, ActivityLog, Notification, Message
from django.contrib.auth.models import User

from datetime import date, datetime

# Assuming `date_obj` is your datetime.date object

jsjey = "/Users/elmaliahmac/Documents/json_keys/serviceAccountKey.json"

cred = credentials.Certificate(jsjey)
firebase_admin.initialize_app(cred)

if not apps:
    firebase_admin.initialize_app(cred)
    
db = firestore.client()

def fire_db(db):
  if db:
    data = (
      # User
      {
        "model": "User",
        "data": User.objects.all().values()
      },
      # UserProfile
      {
        "model": "UserProfile",
        "data": UserProfile.objects.all().values()
      },
      # Post
      {
        "model": "Post",
        "data": Post.objects.all().values()
      },
      # Comment
      {
        "model": "Comment",
        "data": Comment.objects.all().values()
      },
      # Like
      {
        "model": "Like",
        "data": Like.objects.all().values()
      },
      # Follow
      {
        "model": "Follow",
        "data": Follow.objects.all().values()
      },
      # ActivityLog
      {
        "model": "ActivityLog",
        "data": ActivityLog.objects.all().values()
      },
      # Notification
      {
        "model": "Notification",
        "data": Notification.objects.all().values()
      },
      # Message
      {
        "model": "Message",
        "data": Message.objects.all().values()
      }
    )
    for d in data:
      for item in d['data']:
        for key, value in item.items():
          if isinstance(value, date):  # if the value is a date object
            item[key] = datetime.combine(value, datetime.min.time())  # convert it to a datetime object
        db.collection(d['model']).add(item)
      print(f"{d['model']} added to Firestore")
  else:
    raise ValueError("Firestore not initialized") 

  return db,data