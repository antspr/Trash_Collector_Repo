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
    Customer = apps.get_model('customers.Customer')
    return render(request, 'employees/index.html')

@login_required
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        zip_from_form = request.POST.get('zip')
        new_customer = Employee(name=name_from_form, user=logged_in_user, zip_code=zip_from_form)
        new_customer.save()
        return HttpResponseRedirect(reverse('employee:index'))
    else:
        return render(request, 'employee/create.html')
