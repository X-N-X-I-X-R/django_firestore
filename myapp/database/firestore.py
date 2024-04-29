# firestore.py imports
from django import apps
from firebase_admin import credentials, firestore
from myapp.models.models import Post, Comment, Like, Follow, UserProfile, ActivityLog, Notification, Message
from django.contrib.auth.models import User
from datetime import date, datetime

import firebase_admin

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













# סקריפט זה משמש להעברת נתונים מדגמי ה-Django שלך ל-Firestore. להלן הסבר שלב אחר שלב:

# 1. הוא מייבא מודולים נחוצים ומאתחל את Firebase Admin SDK עם מפתח חשבון השירות שלך.

# 2. הוא מגדיר פונקציה `fire_db(db)` שלוקחת לקוח Firestore כארגומנט.
# 3. בתוך פונקציה זו, היא מכינה טופלה `נתונים` המכילה מילונים. כל מילון מייצג מודל Django ומכיל את שם המודל ואת כל המופעים שלו שהומרו למילונים בשיטת `values()`.

# 4. לאחר מכן הוא חוזר על כל מילון ב'נתונים'. עבור כל מילון, הוא חוזר על כל מופע של המודל.
# 5. עבור כל מופע, הוא בודק כל שדה. אם ערך השדה הוא אובייקט תאריך, הוא ממיר אותו לאובייקט תאריך תאריך. הסיבה לכך היא ש-Firestore לא תומכת באובייקטי תאריך, אלא רק באובייקטי תאריך.

# 6. לאחר מכן הוא מוסיף את המופע לאוסף Firestore המתאים באמצעות שיטת `add()`. שם הקולקציה זהה לשם הדוגמנית.

# 7. לאחר שכל המופעים של דגם נוספו ל-Firestore, היא מדפיסה הודעה המציינת שהדגם נוסף ל-Firestore.
# 8. אם לקוח Firestore אינו מאותחל, הוא מעלה 'ValueError'.

# 9. לבסוף, הוא מחזיר את לקוח Firestore ואת ה-'data' tuple.

# סקריפט זה הוא דרך להעביר את כל הנתונים מדגמי ה-Django שלך ל-Firestore. זוהי פעולה חד פעמית ואינה שומרת על אוספי Firestore מסונכרנים עם דגמי ה-Django שלך. אם תוסיף, תעדכן או תמחק מופעים בדגמי ה-Django שלך, תצטרך להפעיל את הסקריפט הזה שוב כדי לשקף את השינויים האלה ב-Firestore.