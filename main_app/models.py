from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
# Book Model
class Book(models.Model):
    api_id = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    image = models.CharField(max_length=1000)
    page_count = models.IntegerField()

    def __str__(self):
        return self.title

# Tea Model
class Tea(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    image_url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.name

# Thread Model
class Thread(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('thread_detail', kwargs={'thread_id': self.id})
    
    class Meta:
        ordering = ['-created_at']

    def last_updated(self):
        last_comment = self.comments.order_by('-created_at').first()
        if last_comment:
            return last_comment.created_at
        return self.created_at


# Comment Model
class Comment(models.Model):
    thread = models.ForeignKey(Thread, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.thread}'
    
    def get_absolute_url(self):
        return reverse('comment_detail', kwargs={'pk': self.id})
    
    class Meta:
        ordering = ['-created_at']
