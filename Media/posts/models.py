from django.db import models
from django.utils import timezone
# Create your models here.

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    postContent = models.CharField()
    created_at = models.CharField(default=timezone.now)
    creator_id = models.IntegerField()
    username = models.CharField(default="anonymous")



class Like(models.Model):
    post_id = models.IntegerField()
    user_id = models.IntegerField()


class Follow(models.Model):
    follower = models.CharField(default="")
    username = models.CharField(default="")