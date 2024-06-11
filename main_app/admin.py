from django.contrib import admin
from .models import Book, Tea, Thread, Comment

# Register your models here.
admin.site.register(Book)
admin.site.register(Tea)
admin.site.register(Thread)
admin.site.register(Comment)
