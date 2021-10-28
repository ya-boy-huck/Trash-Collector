from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
import calendar
from django.db.models import Q
from .models import Employee

@login_required
def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    Customer = apps.get_model('customers.Customer')
    logged_in_employee = request.user
    try:
        logged_in_employee = Employee.objects.get(user=logged_in_employee)
        today = date.today()
        day_of_week = calendar.day_name[today.weekday()]
        pickups_by_zip = Customer.objects.filter(zip_code__contains = logged_in_employee.zip_code) #This grabs all the customers with the employees zipcode
        pickups_by_pickup_date = pickups_by_zip.filter(weekly_pickup = day_of_week) | pickups_by_zip.filter(one_time_pickup = today) #This is where we determine if today is the pickup day or extra pickup 
        pickups_non_suspend = pickups_by_pickup_date.exclude(suspend_start__lt = today, suspend_end__gt = today) #This exclues all suspended accounts
        #confirm sets last pick up.

        context = {
            'logged_in_employee': logged_in_employee,
            'today': today,
            'pickups_by_zip': pickups_by_zip,
            'pickups_by_pickup_date':pickups_by_pickup_date,
            'pickups_non_suspend': pickups_non_suspend 
        }

        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))

@login_required
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        new_employee = Employee(name=name_from_form, user=logged_in_user, zip_code=zip_from_form)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')  


def edit_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        zip_from_form = request.POST.get('zip_code')
        logged_in_employee.name = name_from_form
        logged_in_employee.zip_code = zip_from_form
        logged_in_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request, 'employees/edit_profile.html', context)


def confirm(request, customer_id):
    try:
        Customers = apps.get_model('customers.Customer')
        charge_customer = Customers.objects.get(id =customer_id)
        charge_customer.balance += 20
        charge_customer.date_of_last_pickup = datetime.now()
        charge_customer.save()
        
        return render(request, 'employees/index.html')
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:index'))

def select_day(request):
    user = request.user
    logged_in_employee = Employee.objects.get(user=user)
    Customers = apps.get_model('customers.Customer')
    pickup_customers = Customers.objects.all()
    current_day = str(date.today())
    weekday = request.POST.get('day_of_the_week')
    

    context = { 
                'pickup_customers': pickup_customers,
                'weekday': weekday
    }
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('employees:index'))
    return render(request, 'employees/daily_tasks.html', context)



