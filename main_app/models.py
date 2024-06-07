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
        return self.name

