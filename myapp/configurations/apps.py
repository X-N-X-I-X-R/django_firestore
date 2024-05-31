# apps.py

from django.apps import AppConfig



class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name= 'myapp.configurations' 

    def ready(self):
        import myapp.logic.signals  
        
        # explanation about this file : 
