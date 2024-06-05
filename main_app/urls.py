from django.urls import path
from . import views
	
urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('books/', views.books, name='books'),
    path('tea/', views.tea, name='tea'),
    path('discussion/', views.discussion, name='discussion'),
]