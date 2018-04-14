from django.shortcuts import render, HttpResponseRedirect
from .forms import Shoe
from .forms import ShoeDescriptionByAssessorForm
import os
import random
import subprocess
#from products.models import *

def CreateCatolog(data_path, result_path):
    data = []
    for root, subdirs, files in os.walk(data_path):
        for f in files:
            if os.path.splitext(f)[1].lower() in ('.jpg', '.jpeg'):
                data += [os.path.join(root, f)]
    print(len(data))
    #data = random.sample(data, 50)
    for d in data:
        subprocess.call(['cp', d, result_path + os.path.basename(d)])
        Shoe.objects.create(image="target_products/" + os.path.basename(d))



def product_description(request, shoes_id, user_id):
    title = "Step 3: Describe and remember"

    saw_shoe_description = True
    shoe = Shoe.objects.get(id=shoes_id)
    images = [shoe.image]
    form = ShoeDescriptionByAssessorForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        print(form.cleaned_data)
        new_form = form.save(commit=False)
        new_form.image_id = shoes_id
        new_form.user_profile = user_id
        new_form.save()
        return HttpResponseRedirect("/start_session/" + str(user_id) + "/" + str(shoes_id) + "/")
    return render(request, 'products/description_the_picture.html', locals())

def landing(request, user_id):
    #CreateCatolog("static/media/target_products/", "static/media/target_products/")
    products = Shoe.objects.all()
    ids = [product.id for product in products]
    new_shoes_id = random.choice(ids)
    #new_shoes_id = 26
    return render(request, 'products/task_description.html', locals())
