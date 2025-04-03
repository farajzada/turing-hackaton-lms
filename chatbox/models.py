from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    prompt = models.TextField()
    response = models.TextField()
    model_used = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    chat_id = models.UUIDField(default=uuid.uuid4) 
    title = models.CharField(max_length=100, default="Yeni Chat")
    feedback = models.CharField(max_length=10, choices=[("like", "Like"), ("dislike", "Dislike")], null=True, blank=True)