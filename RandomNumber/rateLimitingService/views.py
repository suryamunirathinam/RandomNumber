from datetime import datetime,timedelta
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
    request.session['limit'] = 5-count['count']
    request.session['hits'] = count['count']
    if request.session['limit'] == 4:
        time = datetime.now()
        request.session['time'] = time.__str__()
        request.session['after']= (time +timedelta(hours=1)).__str__()
    return render(request, 'random_no.html', {
        'randomnumber': rand_no,

    })

@login_required
def remainingLimits(request):
    try:
        datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
        date1 = datetime.now().__str__()
        print(date1)
        date2 = request.session['after']
        print(date2)
        diff = datetime.strptime(date2, datetimeFormat) \
               - datetime.strptime(date1, datetimeFormat)
        print(diff.seconds)
        limit = int(diff.seconds/60)*5 - request.session['hits']
        print(limit)


    except Exception as e:
        print(e)
        limit = 300

    return render(request, 'remaining_limits.html', {
        'Remaininglimit':limit
    })
