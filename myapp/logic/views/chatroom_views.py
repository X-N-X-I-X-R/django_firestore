# from myapp.models.chat_models import ChatRoom, ChatMessage
# from rest_framework import viewsets 
# from rest_framework import serializers

# from rest_framework.decorators import action
# from rest_framework.response import Response

# class ChatRoomSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = ChatRoom
#     fields = ['id', 'title']


# class MessageSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = ChatMessage
#     fields = ['id', 'room', 'user', 'content', 'timestamp']
    
    
# class ChatRoomViewSet(viewsets.ModelViewSet):
#     queryset = ChatRoom.objects.all()
#     serializer_class = ChatRoomSerializer

#     @action(detail=True, methods=['get'])
#     def get_messages(self, request, pk=None):
#         chatroom = self.get_object()
#         messages = ChatMessage.objects.filter(room=chatroom)
#         serializer = MessageSerializer(messages, many=True)
#         return Response(serializer.data)

# class MessageViewSet(viewsets.ModelViewSet):
#     queryset = ChatMessage.objects.all()
#     serializer_class = MessageSerializer

#     @action(detail=True, methods=['get'])
#     def get_chatroom(self, request, pk=None):
#         message = self.get_object()
#         chatroom = ChatRoom.objects.get(id=message.room.id)
#         serializer = ChatRoomSerializer(chatroom)
#         return Response(serializer.data)
        
        
        
        
    