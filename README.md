# Restaurant kitchen service project

Django project for managing dishes and cooks in a restaurant

## Check it out  
https://restaurant-kitchen-service-5gq2.onrender.com/

You can use these test credentials  
login: user  
password: user12345

## Installation
Python 3.11 must be already installed

git clone https://github.com/viktoriaom/restaurant-kitchen-service  
cd restaurant_kitchen_service  
python3 -m venv venv  
source venv/bin/activate # creates virtual environment on macOS/Linux  
venv\Scripts\activate # creates virtual environment on Windows  
pip install -r requirements.txt  
create .env file based on the example  
python manage.py makemigrations # creates migrations  
python manage.py migrate # creates DB  
python manage.py runserver # starts Django server  

## Features
* Authorisation functionality for Cook/User
* Managing dish types, dishes, ingredients and cooks profiles directly from website interface
* Role-based access via Django Groups (trainee, employee, manager)
* Powerful admin panel for advanced managing
* Tests cover all custom features

## Built With
* Django [https://www.djangoproject.com]
* Django Template Pixel (custom styling layer) [https://github.com/app-generator/django-pixel/tree/396e4c3686e02063cfe742ba5a4180c1c23f2f41]

## Usage Tips
* Superusers bypass all group restrictions
* Groups (trainee, employee, manager) are created via Django signals after migration
* Permissions are enforced on views using GroupRequiredMixin
