from django.shortcuts import render

# Create your views here.

# View functions pull from models
# Define the home view
def home(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'home.html')