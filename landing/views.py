from django.shortcuts import render, HttpResponseRedirect
from .forms import AssessorProfileForm, LoginForm, Login, AssessorProfile
#from products.models import *


def landing(request, form_id):
    form = AssessorProfileForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        print(form.cleaned_data)
        new_form = form.save(commit=False)
        new_form.login = int(form_id)
        new_form.save()
        return HttpResponseRedirect("/task_description/" + str(new_form.id) + "/")
    return render(request, 'landing/create_account.html', locals())

def CreateAccount(request, signal):
    if (signal == "0"):
        title = ""
    if (signal == "1"):
        title = "Sorry this user name already exists. Try again."
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        print(form.cleaned_data)
        new_form = form.save(commit=False)
        if Login.objects.filter(user_name = new_form.user_name).exists():
            return HttpResponseRedirect("/create_account/1/")
        form.save()
        return HttpResponseRedirect("/instruction/" + str(new_form.id) + "/")
    return render(request, 'landing/create_account.html', locals())

def login(request, signal):
    if (signal == "0"):
        title = ""
    if (signal == "1"):
        title = "Sorry this combination does not exist. Try again."
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        print(form.cleaned_data)
        new_form = form.save(commit=False)
        profiles = Login.objects.filter(user_name = new_form.user_name, password = new_form.password)
        if (len(profiles) > 0):
            if not AssessorProfile.objects.filter(login=profiles[0].id).exists():
                return HttpResponseRedirect("/instruction/" + str(profiles[0].id) + "/")
            user = AssessorProfile.objects.get(login=profiles[0].id)
            return HttpResponseRedirect("/task_description/" + str(user.id) + "/")
        else:
            return HttpResponseRedirect("/login/1/")
    return render(request, 'landing/login.html', locals())