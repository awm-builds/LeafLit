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
    path('discussion/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('discussion/new_thread/', views.new_thread, name='new_thread'),
    path('discussion/comment/add/<int:thread_id>/', views.add_comment, name='add_comment'),
    path('discussion/comment/<int:pk>/', views.comment_detail, name='comment_detail'),
    path('discussion/comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('discussion/comment/<int:pk>/edit/', views.edit_comment, name='edit_comment'),
]
