from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-published_date']
    def publish(self):
        self.published_date = timezone.now() #sets the published date to the current time
        self.save() #saves the post with the new published date

    def get_absolute_url(self):
         return reverse("post_detail", kwargs={"pk": self.pk}) #returns the URL for the post detail view

    def approve_comments(self):
         return self.comments.filter(approved_comment=True)
    
    def __str__(self):
            return self.title
    
class Comment(models.Model):
     post = models.ForeignKey('Main_Blog.Post', related_name='comments', on_delete=models.CASCADE)
     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
     text = models.TextField()
     created_date = models.DateTimeField(default=timezone.now)
     approved_comment = models.BooleanField(default=False)

     class Meta:
          ordering = ['-created_date']

     def approve(self):
          self.approved_comment = True
          self.save()
     def __str__(self):
        return self.text
     
     def get_absolute_url(self):
          return reverse("post_list")