from django.shortcuts import render, HttpResponseRedirect
from .forms import InterpretabilityForm, \
    InterpretabilityGame, Interpretability
from shoes.views import TakeImageIdFromTask
from landing.forms import Login, LoginForm, AssessorProfile, AssessorProfileForm

from search.views import TakeDatasetFromMethodNumber, GetFeturesFromText, \
    Real1_one_feature_from_given_features, GetFeaturesForOneImage, AnswerForm
import os
import numpy as np
import random
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

n_bins = 5
n_pictures_per_bin = 5
n_features = 5
n_methods = 6
#from products.models import *


def CreateInterpretabilityGame(user_id):
    target_image_id = random.choice(os.listdir("static/media/product/"))
    target_image_id = os.path.basename(target_image_id)
    if InterpretabilityGame.objects.filter(user_id=user_id).exists():
        games = [game for game in InterpretabilityGame.objects.filter(user_id=user_id)]
        for game in games:
            if game.iteration < 20:
                return game
    image_to_choose = random.choice(os.listdir("static/media/product/"))
    image_to_choose = os.path.basename(image_to_choose)

    game = InterpretabilityGame.objects.create(user_id=user_id, target_image=target_image_id, image_to_choose = image_to_choose)
    questions_order = []
    for i in range(1,5):
        l = [i*10 + f for f in range(n_features)]
        questions_order += l
    random.shuffle(questions_order)
    questions_order.append(50)
    game.question_order = "_".join(str(s) for s in questions_order)
    game.save()
    return game

def CreateInterpretabilityGameFromPool(user_id, n_plays_with_one_game, n_iterations):
    if InterpretabilityGame.objects.filter(user_id=user_id).exists():
        games = [game for game in InterpretabilityGame.objects.filter(user_id=user_id)]
        for game in games:
            if game.iteration < 20:
                return game
    existing_games = InterpretabilityGame.objects.filter(game_number = -1)
    free_games = [game.id for game in existing_games if
                  len(InterpretabilityGame.objects.filter(game_number=game.id, iteration=n_iterations)) < n_plays_with_one_game]
    game_id = random.choice(free_games)
    target_image_id = InterpretabilityGame.objects.get(id=game_id).target_image
    image_to_choose = random.choice(os.listdir("static/media/product/"))
    image_to_choose = os.path.basename(image_to_choose)
    game = InterpretabilityGame.objects.create(user_id=user_id, target_image=target_image_id, game_number = game_id,
                                               image_to_choose = image_to_choose)
    questions_order = []
    for i in range(1,5):
        l = [i*10 + f for f in range(n_features)]
        questions_order += l
    random.shuffle(questions_order)
    questions_order.append(50)
    game.question_order = "_".join(str(s) for s in questions_order)
    game.save()
    return game

def RecieveTheWrightAnswer(image,data, data_in_bins):
    for bin in range(n_bins):
        for im in data_in_bins[bin]:
            if data[im].split("_")[-1] == os.path.basename(image):
                return bin


def EndInterpretabilityTask(request, game_id):
    task_code = np.random.randint(0, 1000000)
    game = InterpretabilityGame.objects.get(id=game_id)
    game.code = task_code
    game.save()
    return render(request, 'interpretability/end_interpretability.html', locals())

def ChooseTheColumn(request, game_id):
    buy_button = False
    choose_targert_image = True

    game = InterpretabilityGame.objects.get(id=game_id)
    print("iteration_number = ", game.id)
    iteration = game.iteration
    method_feature = int(game.question_order.split("_")[iteration])
    method_id = method_feature / 10
    feature_n = method_feature % 10
    data1 = open(TakeDatasetFromMethodNumber(method_id)).read()
    features, data = GetFeturesFromText(data1)
    target_image = game.target_image
    if (method_id == 5):
        target_image = "8008094.585.jpg"
    point_features = GetFeaturesForOneImage(target_image, data1)
    print("point features = ", point_features)

    images_in_bins, data_in_bins = \
        Real1_one_feature_from_given_features(features,
                                              data,
                                              n_bins,
                                              n_pictures_per_bin,
                                              feature_n,
                                              point_features,
                                              1)

    class Image:
        def __init__(self, url):
            self.url = url

    class Image_:
        def __init__(self, url):
            self.image = Image(url)

    imgs = []
    for bin in range(n_bins):
        line = []
        for im_n in images_in_bins[bin]:
            im_url = "/media/product/" + data[im_n].split("_")[-1]
            line.append(Image_(im_url))
        imgs.append(line)

    target_image_url = Image_("/media/product/" + game.image_to_choose).image.url
    values = range(n_bins)
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    interpretability_class = Interpretability.objects.get(game_id=game, iteration=game.iteration)
    interpretability = interpretability_class.property
    form = AnswerForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            final_score = form.cleaned_data['Answer']
            interpretability_class.given_answer = int(final_score)
            interpretability_class.wright_answer = RecieveTheWrightAnswer(game.image_to_choose,
                                                                          data, data_in_bins)
            interpretability_class.save()
            game.iteration += 1
            game.save()
            return HttpResponseRedirect("/interpretability_task/" + game_id + "/")


    return render(request, 'search/search.html', locals())



def InterpretabilityFunction(request, game_id):
    print("START")


    game = InterpretabilityGame.objects.get(id=game_id)
    print("iteration_number = ", game.id)
    iteration = game.iteration
    method_feature = int(game.question_order.split("_")[iteration])
    method_id = method_feature / 10
    feature_n = method_feature % 10
    data1 = open(TakeDatasetFromMethodNumber(method_id)).read()
    features, data = GetFeturesFromText(data1)
    target_image = game.target_image
    if (method_id == 5):
        target_image = "8008094.585.jpg"
    point_features = GetFeaturesForOneImage(target_image, data1)
    print("point features = ", point_features)

    images_in_bins, data_in_bins = \
        Real1_one_feature_from_given_features(features,
                                              data,
                                              n_bins,
                                              n_pictures_per_bin,
                                              feature_n,
                                              point_features,
                                              1)

    class Image:
        def __init__(self, url):
            self.url = url

    class Image_:
        def __init__(self, url):
            self.image = Image(url)

    imgs = []
    for bin in range(n_bins):
        line = []
        for im_n in images_in_bins[bin]:
            im_url = "/media/product/" + data[im_n].split("_")[-1]
            line.append(Image_(im_url))
        imgs.append(line)

    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    form = InterpretabilityForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        print(form.cleaned_data)
        new_form = form.save(commit=False)
        new_form.game_id = game
        new_form.iteration = game.iteration
        new_form.feature_n = feature_n
        new_form.method_id = method_id
        new_form.save()
        if (game.iteration >= n_features * 4):
            return HttpResponseRedirect("/end_interpretability_task/" + game_id + "/")
        return HttpResponseRedirect("/choose_column/" + game_id + "/")

    return render(request, 'search/search_interpretability.html', locals())


def StartInterpretabilityTask(request, user_id):
    game = CreateInterpretabilityGame(user_id)
    #game = CreateInterpretabilityGameFromPool(user_id, 1, 21)
    game_id = game.id
    return render(request, 'interpretability/start_interpretability.html', locals())

def landingInterpretability(request, form_id):
    form = AssessorProfileForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        new_form = form.save(commit=False)
        new_form.login = int(form_id)
        new_form.save()

        user = AssessorProfile.objects.get(login=int(form_id))
        return HttpResponseRedirect("/start_interpretability_task/" + str(user.id) + "/")

    return render(request, 'landing/create_account.html', locals())


def CreateAccountInterpretability(request, signal):
    if (signal == "0"):
        title = ""
    if (signal == "1"):
        title = "Sorry this user name already exists. Try again."
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        print(form.cleaned_data)
        new_form = form.save(commit=False)
        if Login.objects.filter(user_name = new_form.user_name).exists():
            return HttpResponseRedirect("/create_account_Interpretability/1/")
        form.save()
        return HttpResponseRedirect("/landing_Interpretability/" + str(new_form.id) + "/")
    return render(request, 'landing/create_account.html', locals())

def loginInterpretability(request, signal):
    if (signal == "0"):
        title = ""
    if (signal == "1"):
        title = "Sorry this combination does not exist. Try again."
    form = LoginForm(request.POST or None)
    redirect_to_create_account = "/create_account_Interpretability/0/"
    if request.method == "POST" and form.is_valid():
        print(form.cleaned_data)
        new_form = form.save(commit=False)
        profiles = Login.objects.filter(user_name = new_form.user_name, password = new_form.password)
        if (len(profiles) > 0):
            user = AssessorProfile.objects.get(login=profiles[0].id)

            if not AssessorProfile.objects.filter(login=profiles[0].id).exists():
                return HttpResponseRedirect("/landing_Interpretability/" + str(profiles[0].id) + "/")
            return HttpResponseRedirect("/start_interpretability_task/" + str(user.id) + "/")
        else:
            return HttpResponseRedirect("/login_Interpretability/1/")
    return render(request, 'landing/login.html', locals())

