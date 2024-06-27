import jwt
import datetime
from django.conf import settings
from django.db import models
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import requests

# יצירת JWT
def create_jwt(user_email, user_name):
    payload = {
        'aud': 'my-app',
        'iss': 'my-app-id',
        'sub': '8x8.vc',
        'room': '*',
        'context': {
            'user': {
                'name': user_name,
                'email': user_email,
                'avatar': 'https://example.com/avatar.png'
            }
        },
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    secret = settings.JWT_SECRET
    token = jwt.encode(payload, secret, algorithm='HS256')
    return token

# יצירת פגישה
def create_meeting():
    token = create_jwt('user@example.com', 'User Name')
    room_name = 'exampleRoom'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.post('https://api.8x8.vc/v1/meetings', json={'name': room_name}, headers=headers)
    return response.json()

# מודל Meeting
class Meeting(models.Model):
    room_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    recording_url = models.URLField(blank=True, null=True)
    transcript = models.TextField(blank=True, null=True)
    
    def __str__(self):  
        return self.room_name

# סריאליזר ל-Meeting
class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'

# ViewSet ל-Meeting
class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    @action(detail=False, methods=['post'])
    def create_meeting(self, request):
        user_email = request.data.get('email')
        user_name = request.data.get('name')
        token = create_jwt(user_email, user_name)
        room_name = request.data.get('room_name', 'exampleRoom')
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = requests.post('https://api.8x8.vc/v1/meetings', json={'name': room_name}, headers=headers)
        if response.status_code == 200:
            meeting_data = response.json()
            meeting = Meeting.objects.create(room_name=room_name)
            return Response({'meeting_id': meeting.id, 'meeting_data': meeting_data}) # type: ignore
        return Response(response.json(), status=response.status_code)

    @action(detail=True, methods=['post'])
    def save_transcript(self, request, pk=None):
        meeting = self.get_object()
        meeting.transcript = request.data.get('transcript')
        meeting.save()
        return Response({'status': 'transcript saved'})

    @action(detail=True, methods=['post'])
    def save_recording(self, request, pk=None):
        meeting = self.get_object()
        meeting.recording_url = request.data.get('recording_url')
        meeting.save()
        return Response({'status': 'recording URL saved'})
