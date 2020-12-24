from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Messages(models.Model):
    message = models.CharField(max_length=50, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message


