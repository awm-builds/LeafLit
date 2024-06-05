from django.db import models

# Create your models here.
# Book Model
class Book(models.Model):
    API_ID = models.CharField(max_length=250)
    book_id = models.IntegerField()
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    image = models.CharField(max_length=250)

    def __str__(self):
        return self.name


