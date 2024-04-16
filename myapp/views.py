

# from django.shortcuts import render
# from .models import UserProfile
# from rest_framework.decorators import api_view 
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import UserProfileSerializers




# @api_view(['GET'])
# def user_list(request):
#   """
#   List all users.
#   """
#   users = UserProfile.objects.all()
#   serializer = UserProfileSerializers(users, many=True)
#   if not users:
#     return Response(status=status.HTTP_404_NOT_FOUND)
#   return render(request, 'user_list.html', {'users': users})



