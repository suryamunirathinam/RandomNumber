import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from ratelimit.decorators import ratelimit
import random
from ratelimit.core import get_usage

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form
    })

@login_required
@ratelimit(key='post:username', rate='5/m', block=True)
def generate_rand_no(request):
    rand_no = random.randint(1, 9999)
    count = get_usage(request, group=None,fn=generate_rand_no, key ='post:username', method='GET', rate = '5/m',increment=True)
    request.session['limit']=5-count['count']
    if request.session['limit'] == 4:
        request.session['time'] = datetime.datetime.now().__str__()
    return render(request, 'random_no.html', {
        'randomnumber': rand_no,
    })

@login_required
def remainingLimits(request):
    try:
        datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
        date1 = request.session['time']
        date2 = datetime.datetime.now().__str__()
        diff = datetime.datetime.strptime(date2, datetimeFormat) \
               - datetime.datetime.strptime(date1, datetimeFormat)
        print (diff.seconds)
        if diff.seconds > 60:

            limit = 5
        else:
            limit = request.session['limit']
    except Exception as e:
        print(e)
        limit = 5

    return render(request, 'remaining_limits.html', {
        'Remaininglimit':limit
    })
