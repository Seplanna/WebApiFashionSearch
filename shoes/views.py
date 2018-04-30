from django.shortcuts import render, HttpResponseRedirect
from .forms import Shoe
from .forms import ShoeDescriptionByAssessorForm, OneTask,ShoeDescriptionByAssessor
import os
import random
import subprocess
#from products.models import *

def ChooseTask(user_id):
    n_images = 6

    if (OneTask.objects.filter(user_id=user_id).exists()):
        tasks = OneTask.objects.filter(user_id=user_id)
        print(len(tasks), [task.id for task in tasks])
        tasks_not_finished = [task for task in tasks if task.iteration < n_images]
        if len(tasks_not_finished) > 0:
            return tasks_not_finished[0]


    used_tasks = [task_number.task_number for task_number in OneTask.objects.all() if
                  task_number.iteration == n_images]
    all_tasks = open("static/text_files/tasks1.txt").readlines()[:-1]
    free_tasks = [i for i in range(len(all_tasks)) if i not in used_tasks]
    if len(free_tasks) == 0:
        free_tasks = [i for i in range(len(all_tasks))]
    task_number = random.choice(free_tasks)
    task = all_tasks[task_number].strip().split("\t")
    images = "\t".join(task[:n_images])
    methods = "\t".join(task[n_images:])
    return OneTask.objects.create(images=images, methods=methods, task_number=task_number, user_id=user_id)

def TakeImageIdFromTask(task):
    image = task.images.split("\t")[task.iteration]
    if not Shoe.objects.filter(image=("target_products/" + image)).exists():
        Shoe.objects.create(image=("target_products/" + image))
    product = Shoe.objects.get(image=("target_products/" + image))
    return product.id

def CreateCatolog(data_path):
    data = []
    for root, subdirs, files in os.walk(data_path):
        for f in files:
            if os.path.splitext(f)[1].lower() in ('.jpg', '.jpeg'):
                data += [os.path.join(root, f)]
    print(len(data))
    for d in data:
        Shoe.objects.create(image="target_products/" + os.path.basename(d))

def product_description(request, task_id, user_id):
    title = "Step 3: Describe and remember"

    saw_shoe_description = True
    task = OneTask.objects.get(id=task_id)
    shoe_id = TakeImageIdFromTask(task)
    shoe = Shoe.objects.get(id=shoe_id)
    images = [shoe.image]

    form = ShoeDescriptionByAssessorForm(request.POST or None)
    if ShoeDescriptionByAssessor.objects.filter(user_profile=user_id, image_id=shoe_id).exists():
        initial_description = ShoeDescriptionByAssessor.objects.filter(user_profile=user_id,
                                                                       image_id=shoe_id)[0]
        form["short_description"].initial = initial_description.short_description
        form["will_you_buy_it_for_your_self"].initial = initial_description.will_you_buy_it_for_your_self
    if request.method == "POST" and form.is_valid():
        print(form.cleaned_data)
        new_form = form.save(commit=False)
        new_form.image_id = shoe_id
        new_form.user_profile = user_id
        new_form.save()
        return HttpResponseRedirect("/start_session/" + str(user_id) + "/" + str(task_id) + "/")
    return render(request, 'products/description_the_picture.html', locals())

def landing(request, user_id):
    if not Shoe.objects.exists():
        CreateCatolog("static/media/target_products/")
    task = ChooseTask(user_id)
    #task.images="8049001.3.jpg\t8049001.3.jpg\t8049001.3.jpg\t8049001.3.jpg\t8049001.3.jpg"
    #task.methods = "5\t5\t5\t5\t5"
    #task.save()
    task_id = task.id

    return render(request, 'products/task_description.html', locals())
