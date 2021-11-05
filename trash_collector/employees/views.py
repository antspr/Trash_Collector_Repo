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
    scheduled_customers = []
    customers_that_share_pickup_day = []
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    today = date.today()
    day_name = today.strftime("%A")
    day_name = day_name.upper()
    try:
        for customer in all_customers:
            if customer.date_of_last_pickup != today:
                if customer.weekly_pickup == day_name:
                    if customer.suspend_start == None and customer.suspend_end == None:
                        scheduled_customers.append(customer)
                    elif today > customer.suspend_start and today < customer.suspend_end:
                        scheduled_customers.append(customer)
        context = {   
            'logged_in_employee': logged_in_employee,
            'today': today,
            'all_customers': all_customers,
            'day_name': day_name,
            'scheduled_customers': scheduled_customers,
            'customers_that_share_pickup_day': customers_that_share_pickup_day,
                    }
        if request.method == 'POST':
            employee_selection = request.POST['pickup_day_drop_down']
            for customer in all_customers:
                if customer.weekly_pickup == employee_selection:
                    customers_that_share_pickup_day.append(customer)
            if customers_that_share_pickup_day != None:
                context.update({'customers_that_share_pickup_day': customers_that_share_pickup_day})
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

       
