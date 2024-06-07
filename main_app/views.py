import os
from .models import Book
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
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
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'discussion.html')

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