from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
import datetime

from django.db.models.fields import DateTimeField

class IpModel(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip
    

class Blog(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    desc = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True)
    likes = models.ManyToManyField(IpModel, related_name="blog_like", blank=True)
    category = models.CharField(max_length=50, default="")
    

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '%s - %s' %(self.blog.title, self.name)
        
    