from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message}'


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    phrase=models.CharField(max_length=200,null=True)
    ai_image=models.ImageField(upload_to='images',null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return str(self.phrase)