from django.contrib import admin
from django.urls import path
from . import views
	
urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('books/', views.books, name='books'),
    path('tea/', views.tea, name='tea'),
    path('discussion/', views.discussion, name='discussion'),
    path('search/books/', views.book_search, name='book_search'),
    path('search/tea/', views.tea_search, name='tea_search'),
    path('books/<str:api_id>/', views.book_detail, name='book_detail'),
    path('tea/<int:tea_id>/', views.tea_detail, name='tea_detail'),
    # check this ^^^^^^^
]