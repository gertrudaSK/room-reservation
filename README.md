# Reservation Program
========================

The Meeting Room Reservation Program for Companies

# Installation

git clone https://github.com/gertrudaSK/room-reservation.git

create the file 'email_settings.py' in \room-reservation\meetings\meetings and put your email settings:

    email = 'your_email@gmail.com'
    email_password = 'your_email_pasword'
    
$ python3 -m venv venv

(env)$ pip install -r requirements.txt

(env)$ python manage.py makemigrations

(env)$ python manage.py migrate

(env)$ python manage.py runserver
