from django.shortcuts import render
from django.http import JsonResponse
from . import rankings
from datetime import datetime as dt
from datetime import timedelta
from home.models import CoderOfTheMonthJSON


try:
    JSON_CACHE = CoderOfTheMonthJSON.objects.latest('time').json   # Just for backup, if database is not working
    print('JSON_CACHE is set')
except:
    print(f'{dt.now()} | Could not fetch JSON from database')
    JSON_CACHE = '{"1":[],"2":[],"3":[],"4":[]}'

MONTH_NAME = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def team(request):
    return render(request, 'team.html')

def coders(request):
    global JSON_CACHE # Get the latest JSON data from the database
    try:
        JSON_CACHE = CoderOfTheMonthJSON.objects.latest('time').json
    except:
        print(f'{dt.now()} | Could not fetch JSON from database')
    month = (dt.now() - timedelta(days=rankings.DAYS_OFFSET)).month
    month = MONTH_NAME[month-1]
    
    return render(request, 'coders.html', context={'json': JSON_CACHE, 'month': month})

def events(request):
    return render(request, 'events.html')

def updateCoders(request):
    print(f'{dt.now()} | Updating coders...')
    json_str = rankings.getJSON()
    if not json_str:
        return JsonResponse({'status': 'error', 'message': 'Could not fetch data from Codeforces'})
    
    try:
        CoderOfTheMonthJSON.objects.create(json=json_str)
    except:
        return JsonResponse({'status': 'error', 'message': 'Could not update database', 'json': json_str})
    
    return JsonResponse({'status': 'success', 'message': 'Successfully updated database', 'time': str(dt.now()), 'json': json_str})
