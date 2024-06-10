import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Book, Tea, Thread, Comment
from .forms import ThreadForm, CommentForm
import requests

# Create your views here.

API_KEY = os.environ['API_KEY']

# View functions pull from models
# Define the home view
def home(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'home.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def books(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'books/books.html')

def tea(request):
  teas = Tea.objects.all()
  return render(request, 'tea/tea.html', {'teas':teas})

def discussion(request):
    threads = Thread.objects.all().order_by('-created_at')
    return render(request, 'discussion/discussion.html', {'threads': threads})

def book_search(request):
  search = request.GET.get('search')
  response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=intitle:{search}&key={API_KEY}')
  data = response.json()['items']
  return render(request, 'books/book_search_results.html', {'book_results': data})

def tea_search(request):
  search = request.GET.get('search')
  teas = Tea.objects.filter(name_icontains=search)
  return render(request, 'tea/tea_search_results.html', {'tea_results': teas})

def book_detail(request, api_id):
  book = Book.objects.filter(api_id=api_id)
  if len(book):
    book = book[0]
  else:
    # Look up book from API
    response = requests.get(f'https://www.googleapis.com/books/v1/volumes/{api_id}?key={API_KEY}')
    print(response.json())
    data = response.json()['volumeInfo']
    # Add book to database
    book = Book.objects.create(
      api_id=api_id,
      title=data['title'],
      author=', '.join(data['authors']),
      description=data['description'],
      image=data['imageLinks']['thumbnail'],
      page_count=data['pageCount'],
    )
  return render(request, 'books/details.html', {
    'book': book,
  })

def tea_detail(request, tea_id):
  tea = get_object_or_404(Tea, id=tea_id)
  return render(request, 'tea/details.html', {
    'tea': tea,
  })

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    comments = thread.comments.all().order_by('-created_at')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.thread = thread
            comment.user = request.user
            comment.save()
            return redirect('thread_detail', thread_id=thread.pk)
    else:
        comment_form = CommentForm()
    
    return render(request, 'discussion/thread_detail.html', {
        'thread': thread,
        'comments': comments,
        'comment_form': comment_form
    })

def new_thread(request):
    if request.method == 'POST':
        thread_form = ThreadForm(request.POST)
        if thread_form.is_valid():
            thread = thread_form.save(commit=False)
            thread.user = request.user
            thread.save()
            return redirect('discussion')
    else:
        thread_form = ThreadForm()
    return render(request, 'discussion/thread_form.html', {'thread_form': thread_form})

def comment_detail(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    return render(request, 'discussion/comment_detail.html', {'comment': comment})

def add_comment(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.thread = thread
            comment.user = request.user
            comment.save()
            return redirect('thread_detail', thread_id=thread.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'discussion/comment_form.html', {'comment_form': comment_form, 'thread': thread})

def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            comment_form.save()
            return redirect('thread_detail', thread_id=comment.thread.pk)
    else:
        comment_form = CommentForm(instance=comment)
    return render(request, 'discussion/comment_form.html', {'comment_form': comment_form, 'comment': comment})

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        thread_pk = comment.thread.pk
        comment.delete()
        return redirect('thread_detail', thread_id=thread_pk)
    comment_form = CommentForm(instance=comment)
    return render(request, 'discussion/comment_form.html', {
        'comment_form': comment_form,
        'comment': comment,
        'is_delete': True
    })