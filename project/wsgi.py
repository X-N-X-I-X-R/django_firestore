import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_wsgi_application()

# gunicorn --bind 0.0.0.0:8989 --workers 9 --worker-class gevent project.wsgi:application

# curl -X GET http://localhost:8989/api/profiles/ -H "accept: application/json"

# curl -X POST http://localhost:8989/api/register_user/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"username\":\"nirprime\",\"email\":\"




'''
סוגי העובדים ב-Gunicorn מוגדרים בצורה מפורשת בקובץ ההגדרות של Gunicorn או דרך פרמטרים בשורת הפקודה בעת הפעלת השרת. ברירת המחדל היא `sync` workers, אבל ניתן להגדיר סוגי עובדים אחרים כמו `gevent` או `eventlet` כדי לקבל ביצועים טובים יותר במצבים מסוימים.

### הגדרת סוגי עובדים בשורת הפקודה

כדי להגדיר סוגי עובדים בעת הפעלת Gunicorn בשורת הפקודה, השתמש בפרמטר `-k` או `--worker-class`. הנה דוגמאות לשימוש בפרמטר זה עם סוגי עובדים שונים:

#### Sync Workers (ברירת מחדל)
אין צורך להגדיר באופן מפורש את סוג העובד, כיוון שברירת המחדל היא `sync`:
```sh
gunicorn --bind 0.0.0.0:8000 --workers 9 project.wsgi:application
```

#### Async Workers עם gevent
```sh
gunicorn --bind 0.0.0.0:8000 --workers 9 --worker-class gevent project.wsgi:application
```

#### Async Workers עם eventlet
```sh
gunicorn --bind 0.0.0.0:8000 --workers 9 --worker-class eventlet project.wsgi:application
```

#### Thread Workers
```sh
gunicorn --bind 0.0.0.0:8000 --workers 9 --threads 3 project.wsgi:application
```

### הגדרת סוגי עובדים בקובץ הגדרות Gunicorn

ניתן גם להגדיר את סוגי העובדים בקובץ הגדרות Gunicorn. יצירת קובץ הגדרות נפרד ושימוש בפרמטר `-c` או `--config` להפעלת Gunicorn עם הקובץ הזה. 

#### דוגמה לקובץ הגדרות Gunicorn (gunicorn_config.py)
```python
bind = "0.0.0.0:8000"
workers = 9
worker_class = "gevent"  # סוג העובדים
```

הפעלת Gunicorn עם קובץ הגדרות:
```sh
gunicorn -c gunicorn_config.py project.wsgi:application
```

### סיכום

- סוגי העובדים ב-Gunicorn מוגדרים בצורה מפורשת בקובץ ההגדרות של Gunicorn או דרך פרמטרים בשורת הפקודה.
- ניתן לבחור בין `sync`, `gevent`, `eventlet` וסוגי עובדים נוספים.
- כדי להגדיר את סוג העובד, השתמש בפרמטר `-k` או `--worker-class` בשורת הפקודה או הגדר את המשתנה המתאים בקובץ ההגדרות.

שימוש נכון בסוגי העובדים וכמות העובדים יסייע לשיפור הביצועים והשרידות של השרת.



'''