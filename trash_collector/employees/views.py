from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from datetime import date

from .models import Employee

# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.


def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    Customers = apps.get_model('customers.Customer')
    all_customers = Customers.objects.all()
    # The following line will get the logged-in user (if there is one) within any view function
    logged_in_user = request.user
    try:
        # This line will return the employee record of the logged-in user if one exists
        logged_in_employee = Employee.objects.get(user=logged_in_user)

        today = date.today()
        day_name = today.strftime("%A")
        day_name = day_name.upper()

        context = {
            'logged_in_employee': logged_in_employee,
            'today': today,
            'all_customers': all_customers,
            'day_name': day_name,
        }
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))


@login_required
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        zip_from_form = request.POST.get('zip_code')
        new_employee = Employee(name=name_from_form, user=logged_in_user, zip_code=zip_from_form)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')


@login_required
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


@login_required
def confirm_pickup(request, customer_id):
    Customers = apps.get_model('customers.Customer')
    customer = Customers.objects.get(id=customer_id)
    today = date.today()
    customer.date_of_last_pickup = today
    customer.balance -= 20
    customer.save()
    return HttpResponseRedirect(reverse('employees:index'))


def view_pickups(request):
    Customers = apps.get_model('customers.Customer')
    all_customers = Customers.objects.all()
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    today = date.today()
    day_name = today.strftime("%A")
    day_name = day_name.upper()
    customers_that_share_pickup_day = []
    employee_selection = request.POST['pickup_day_drop_down']
    try:
        for customer in all_customers:
            if customer.weekly_pickup == employee_selection:
                customers_that_share_pickup_day.append(customer)
                context = {
                'logged_in_employee': logged_in_employee,
                'all_customers': all_customers,
                'customers_that_share_pickup_day': customers_that_share_pickup_day,
                'today': today,
                'day_name': day_name
                }
                if customers_that_share_pickup_day != None:
                    return render(request, 'employees/index.html', context)
                else:
                    return HttpResponseRedirect(reverse('employees:index'))
            else:
                return HttpResponseRedirect(reverse('employees:index'))
    except(ValueError):
        return HttpResponseRedirect(reverse('employees:index'))
       
