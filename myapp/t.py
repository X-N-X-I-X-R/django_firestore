import os
import sys
from django.core.wsgi import get_wsgi_application
from django.core.mail import send_mail

sys.path.insert(0, '/Users/elmaliahmac/Documents/Full_stack/Django_server')
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

application = get_wsgi_application()

send_mail(
  '',
  'This is a test email.',
  'the-farm@outlook.co.il',
  ['nirstam@gmail.com'],
  fail_silently=False,
)