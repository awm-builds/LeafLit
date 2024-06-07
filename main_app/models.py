from django.db import models

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

