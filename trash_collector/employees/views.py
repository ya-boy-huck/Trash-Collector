from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
import calendar
from django.db.models import Q
from trash_collector.customers.models import Customer
from .models import Employee


@login_required
def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    Customer = apps.get_model('customers.Customer')
    logged_in_employee = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_employee)
    try:
        logged_in_employee = Employee.objects.get(user=logged_in_employee)
        
        today = date.today()
        day_of_week = figure_out_day(today)
        pickups = Customer.objects.filter(zip_code = logged_in_employee.zip_code) #This grabs all the customers with the employees zipcode
        pickups = pickups.objects.filter(Q(suspend_start__gt = today) | Q(suspend_end__lt = today)) #This exclues all suspended accounts
        pickups = pickups.objects.filter(Q(weekly_pick = day_of_week) | Q(one_time_pickup = day_of_week)) #This is where we determine if today is the pickup day or extra pickup 




        context = {
            'logged_in_employee': logged_in_employee,
            'today': today,
            'pickups' : pickups
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


def display_customer_info(request):
    logged_in_user = request.user
    Customer = apps.get_model('customers.Customer')
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    employees_customer_list = Customer.object.filter(zip_code = logged_in_employee.zip_code)
    
    context = {
            'employees_customer_list': employees_customer_list,
            'logged_in_employee': logged_in_employee
    }
    return render(request, 'employees/index.html', context)

def select_day(request):
    user = request.user
    logged_in_employee = Employee.objects.get(user=user)
    Customers = apps.get_model('customers.Customer')
    pickup_customers = Customers.objects.all()
    current_day = str(date.today())
    weekday = request.POST.get('day_of_the_week')
    pickups = []

    context = { 'pickups': pickups,
                'pickup_customers': pickup_customers,
                'weekday': weekday
    }
    #if request.method == 'POST':
        #return('employees:confirm')
    return render(request, 'employees/daily_view.html', context)


def figure_out_day(day):
    return calendar.day_name[day.weekday()] 