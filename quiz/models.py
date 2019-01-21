from django.db import models
from django.conf import settings


# Create your models here.
class leaderboard(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,primary_key=True)
    score = models.IntegerField(default=None,null=True)
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True,null=True)
    finished_at = models.DateTimeField(default=None,null=True)

class questions(models.Model):
    q_no = models.CharField(max_length=150,primary_key=True)
    title = models.CharField(max_length=150,default=None,null=True)
    content = models.TextField(null=True,default=None)

class answers(models.Model):
    q = models.CharField(max_length=150,primary_key=True)
    ans = models.CharField(max_length=150,default=None,null=True)