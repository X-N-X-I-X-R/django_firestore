# from django.db import models



# from django.contrib.auth import get_user_model

# User = get_user_model()

# class ChatRoom(models.Model):
#   title = models.CharField(max_length=255)

#   def __str__(self):
#     return self.title


# class ChatMessage(models.Model):  
#   room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
#   user = models.ForeignKey(User, on_delete=models.CASCADE)
#   content = models.TextField()
#   timestamp = models.DateTimeField(auto_now_add=True)

#   def __str__(self):
#     return self.content