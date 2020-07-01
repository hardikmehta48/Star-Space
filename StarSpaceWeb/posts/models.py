from django.db import models
from django.urls import reverse
from django.conf import settings

from groups.models import Group

from django.contrib.auth import get_user_model
User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=30)
    message = models.TextField()
    # message_html = models.TextField(editable = False)
    group = models.ForeignKey(Group, related_name='posts', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # self.message_html = misika.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username':self.user.username, 'pk':self.pk} )

    class Meta:
        ordering = ['-created_date']
        unique_together = ['user','message']

class Comments(models.Model):
    user = models.ForeignKey(User, related_name='comments_all', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    message = models.TextField()
    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        # self.message_html = misika.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username':self.post.user.username, 'pk':self.post.pk} )

    class Meta:
        ordering = ['-created_date']
        unique_together = ['user','message']
