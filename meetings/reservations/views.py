from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib import messages
from django.contrib.auth.forms import User
from .models import Rooms, Reservations, Employee
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin


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
        room = int(request.POST['room'])
        date = request.POST['datepicker']
        time_from = request.POST['timepicker1']
        time_due = request.POST['timepicker2']
        employee = request.user.id
        print(room, date, time_from, time_due, employee)
        Reservations.objects.create(room_id_id=room, employee_id_id=employee, date=date, time_from=time_from, time_due=time_due)
        messages.success(request, "The reservation successfully created!")
        return render(request, 'index.html')
    rooms = Rooms.objects.all()
    context = {
    'rooms': rooms
    }
    return render(request, 'room_select.html',context=context)

@login_required
def reservations_list(request):
    paginator = Paginator(Reservations.objects.order_by('-date').all(), 5)
    page_number = request.GET.get('page')
    reservations = paginator.get_page(page_number)
    employees = Employee.objects.all()

    context = {
        'reservations': reservations,
        'employees': employees
    }
    return render(request, 'reservations_ListView.html', context=context)


def search(request):
    query = request.GET.get('query')
    search_results = Reservations.objects.filter(Q(employee_id__name__icontains=query))
    context = {
        'reservations': search_results,
        'query': query,
    }
    return render(request, 'search.html', context=context)

def cancel_reservation(request, id):
    Reservations.objects.filter(id=id).delete()
    messages.success(request, "The reservation successfully canceled!")
    return reservations_list(request)

class RoomCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Rooms
    fields = ['name',]
    success_url = "/reservations/"
    template_name = 'room_CreateView.html'
    success_message = "The meeting room was created successfully"

def room_availability(request):
    datetime_now = datetime.now()
    rooms = Rooms.objects.all()







