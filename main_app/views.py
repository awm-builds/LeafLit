import os
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
  return render(request, 'books.html')

def tea(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'tea.html')

def discussion(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'discussion.html')

def book_search(request):
  search = request.GET.get('search')
  response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=intitle:{search}&key={API_KEY}')
  data = response.json()
  return render(request, 'book_search_results.html', {'book_results': data})
