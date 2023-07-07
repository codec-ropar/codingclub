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
    return render(request, 'home/index.html')

def login(request):
    return render(request, 'home/login.html')

def signup(request):
    return render(request, 'home/signup.html')

def team(request):
    return render(request, 'home/team.html')

def coders(request):
    # Get the latest JSON data from the database
    global JSON_CACHE
    try:
        JSON_CACHE = CoderOfTheMonthJSON.objects.latest('time').json
    except:
        print(f'{dt.now()} | Could not fetch JSON from database')
    month = (dt.now() - timedelta(days=rankings.DAYS_OFFSET)).month
    month = MONTH_NAME[month-1]
    return render(request, 'home/coders.html', context={'json': JSON_CACHE, 'month': month})

def events(request):
    return render(request, 'home/events.html')

def alumni(request):
    return render(request, 'home/alumni.html')


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


updateCoders(None)
exit()