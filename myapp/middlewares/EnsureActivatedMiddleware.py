# EnsureActivatedMiddleware.py 
# pwd = /Users/elmaliahmac/Documents/Full_stack/Django_server/myapp/middlewares/EnsureActivatedMiddleware.py

from django.shortcuts import redirect
from django.urls import reverse

class EnsureActivatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_active:
            return redirect(reverse('activate_prompt'))
        response = self.get_response(request)
        return response


from django.contrib.auth.models import AnonymousUser

class SwaggerBypassAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/swagger/'):
            request.user = AnonymousUser()
        return self.get_response(request)
