Sentry explanation 
================== 
Sentry is a tool that helps you monitor and fix crashes in real time. 
The SDKs automatically report errors and crashes to Sentry, 
where you can see exactly what’s causing them. 
 Sentry is a tool in the  -Exception Monitoring-  category of a tech stack. 

-------------------------------------------------------------------

 Key points :
* Sentry is an open source tool 
* Sentry is a tool that helps you monitor and fix crashes in real time.
* The SDKs automatically report errors and crashes to Sentry, where you can see exactly what’s causing them.   
 - sdk = software development kits

-------------------------------------------------------------------

References :
* https://sentry.io/welcome/
* https://sentry.io/for/exception-monitoring/
React - https://docs.sentry.io/platforms/javascript/guides/react/ 
Angular - https://docs.sentry.io/platforms/javascript/guides/angular/
Vue - https://docs.sentry.io/platforms/javascript/guides/vue/
Node - https://docs.sentry.io/platforms/node/
Python - https://docs.sentry.io/platforms/python/ 


-------------------------------------------------------------------
DJANGO WITH SENTRY 
-------------------------------------------------------------------
 1- install Sentry in Django  :
 * pip install --upgrade 'sentry-sdk[django]'

2-  configure Sentry in Django  :
* sing up in sentry.io , create a project and get the DSN key 
* add the following code in the settings.py file
* install decouple : pip install python-decouple
* create a .env file and add the SENTRY_DSN key

.. import sentry_sdk 
.. from sentry_sdk.integrations.django import DjangoIntegration
.. from decouple import config 
.. from decouple import AutoConfig
.. config = AutoConfig()
.. SENTRY_DSN = config('SENTRY_DSN')
.. sentry_sdk.init(
..     dsn=SENTRY_DSN,
..     integrations=[DjangoIntegration()]


3 - Test Sentry in Django  :
* Try to raise an exception in the views.py file 
* Check the sentry.io dashboard to see the exception


4 - create cron monitoring in sentry  : 
* create a cron job in the server to check the sentry project every 5 minutes 
* if there is an error, send an email to the developer


