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
                    messages.success(request, f"Congratulations - now you can log in!")
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
        time_to = request.POST['timepicker2']
        employee = request.user.id
        time_clean = datetime.strptime(time_from, "%H:%M")
        if time_from > time_to:
            messages.warning(request, "Please select the correct time")
            return redirect('select_room')

        check_rooms = Reservations.objects.filter(room_id=room).filter(date__gte=datetime.now().date()).all()
        for booked in check_rooms:
            if str(booked.date) == str(date):
                if time_in_range(booked.time_from, booked.time_to,
                                 datetime.strptime(time_from, "%H:%M").time()) or time_in_range(booked.time_from,
                                                                                                booked.time_to,
                                                                                                datetime.strptime(
                                                                                                        time_to,
                                                                                                        "%H:%M").time()):
                    messages.warning(request,
                                     "This time is already taken, please check the schedule and select another one.")
                    return redirect('select_room')

        Reservations.objects.create(room_id_id=room, employee_id_id=employee, date=date, time_from=time_from,
                                    time_to=time_to)
        messages.success(request, "The reservation successfully created!")
        return render(request, 'index.html')
    rooms = Rooms.objects.all()
    context = {
        'rooms': rooms
    }
    return render(request, 'room_select.html', context=context)


@login_required
def reservations_list(request):
    paginator = Paginator(Reservations.objects.filter(date__gte=datetime.now().date()).exclude(status="x").order_by('date').all(), 5)
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
    search_results = Reservations.objects.filter(Q(employee_id__name__icontains=query)).filter(
        date__gte=datetime.now().date()).order_by('date').all()
    context = {
        'reservations': search_results,
        'query': query,
    }
    return render(request, 'search.html', context=context)


def cancel_reservation(request, id):
    Reservations.objects.filter(id=id).update(status="x")
    messages.success(request, "The reservation successfully canceled!")
    return reservations_list(request)


class RoomCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Rooms
    fields = ['title', ]
    success_url = "/reservations/"
    template_name = 'room_CreateView.html'
    success_message = "The meeting room was created successfully"


def time_in_range(start, end, x):
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


def room_availability(request):
    all_rooms = Rooms.objects.all()
    all_rooms_list = []
    rooms_all = Reservations.objects.all()
    datetime_now = datetime.now()

    for room in rooms_all:
        check_time = datetime.strptime(str(room.date) + " " + str(room.time_from), "%Y-%m-%d %H:%M:%S")
        check_time_to = datetime.strptime(str(room.date) + " " + str(room.time_to), "%Y-%m-%d %H:%M:%S")
        if check_time < datetime_now and check_time_to < datetime_now:
            Reservations.objects.filter(id=room.id).update(status='d')

    for r in all_rooms:
        all_rooms_list.append(r.title)

    datetime_now = datetime.now().date()
    rooms = Reservations.objects.filter(date=datetime_now).all()
    time_now = datetime.now().time()
    for booked in rooms:
        if time_in_range(booked.time_from, booked.time_to, time_now):
            all_rooms_list.remove(booked.room_id.title)
    context = {
        'available_rooms': all_rooms_list,
    }

    return render(request, 'rooms_avaiable.html', context=context)
