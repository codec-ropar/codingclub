from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'home/index.html')

def login(request):
    return render(request, 'home/login.html')

def signup(request):
    return render(request, 'home/signup.html')

def team(request):
    return render(request, 'home/team.html')

def coders(request):
    return render(request, 'home/coders.html')

def events(request):
    return render(request, 'home/events.html')

def alumni(request):
    return render(request, 'home/alumni.html')