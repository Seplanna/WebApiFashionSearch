from django.shortcuts import render, HttpResponseRedirect
from .forms import AssessorProfileForm
#from products.models import *


def landing(request):
    form = AssessorProfileForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        print(form.cleaned_data)
        new_form = form.save(commit=False)
        form.save()
        return HttpResponseRedirect("/task_description/" + str(new_form.id) + "/")
    return render(request, 'landing/landing.html', locals())

