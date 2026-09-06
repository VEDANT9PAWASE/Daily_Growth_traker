# Self Growth Tracker - Django Project

A simple Django web app to build discipline and track self-growth habits.

## Features

- User signup, login, and logout
- Personal dashboard
- Create, edit, and delete habits
- Mark today's habits as complete/incomplete
- Track current habit streaks
- Daily reflection with discipline score, mood, wins, and improvement notes
- Simple responsive UI

## Setup

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser   # optional
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Default pages

- `/` dashboard
- `/accounts/login/` login
- `/accounts/logout/` logout through POST form
- `/accounts/signup/` signup
- `/habits/new/` add habit

