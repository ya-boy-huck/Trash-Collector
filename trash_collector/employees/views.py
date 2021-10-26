from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from .models import Employee


@login_required
def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers

    Customer = apps.get_model('customers.Customer')
    logged_in_user = request.user
    try:
        logged_in_employee = Employee.objects.get(user=logged_in_user)
        
        today = date.today()

        context = {
            'logged_in_employee': logged_in_employee,
            'today': today
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
        new_employee = Employee(name=name_from_form, user=logged_in_user, address=address_from_form, zip_code=zip_from_form)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')  


def edit_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        logged_in_employee.name = name_from_form
        logged_in_employee.address = address_from_form
        logged_in_employee.zip_code = zip_from_form
        logged_in_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request, 'employee/edit_profile.html', context)



    #  for customer in pickup_customers: 
    #      customer_start_suspension = str(customer.start_suspension)
    #      customer_end_suspension = str(customer.end_suspension)
    #      if  current_day < customer_start_suspension or current_day > customer_end_suspension:     
    #          if customer.zip_code == logged_in_employee.zip_code and (customer.weekly_pickup_date == weekday or customer.extra_pickup_date == weekday) :
    #              pickups.append(customer)




