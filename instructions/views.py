from django.shortcuts import render, HttpResponseRedirect
#from products.models import *


def instruction(request):
    return render(request, 'instructions/task_description.html', locals())

