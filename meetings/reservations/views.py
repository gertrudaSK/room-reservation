from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib import messages
from django.contrib.auth.forms import User
from .models import Rooms


def index(request):
    return render(request, 'index.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'User name {username} is already exists!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'{email} is already exists!')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.success(request, f"Congratulations - now you can sign in!")
                    return redirect('index')
        else:
            messages.error(request, 'The passwords have to match!')
            return redirect('register')
    return render(request, 'register.html')

@csrf_exempt
@login_required
def select_room(request):
    if request.method == 'POST':
       room = request.POST['room']

    else:
        rooms = Rooms.objects.all()
        context = {
            'rooms': rooms
        }
    return render(request, 'room_select.html', context=context)




