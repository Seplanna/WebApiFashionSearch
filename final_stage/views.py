from django.shortcuts import render, HttpResponseRedirect
from .forms import OneImage, Game, Shoe, ShoeDescriptionByAssessor, Login, AssessorProfile, OneTask
import os
import numpy as np
#from products.models import *
def Copy_logins_and_Profiles(path_login, path_user_profile):
    logins = Login.objects.all()
    with open(path_login, 'w') as login_file, open(path_user_profile, 'w') as user_file:
        for login in logins:
            login_file.write(str(login.id) + "\t" + str(login.user_name) + "\t" +
                             str(login.password) + "\n")
            if (AssessorProfile.objects.filter(login=login.id).exists()):
                a_p = AssessorProfile.objects.get(login=login.id)
                user_file.write(str(a_p.id) + "\t" + str(a_p.login) + "\t" + str(a_p.career_field) +
                                "\t" + str(a_p.gender) + "\t" + str(a_p.age) + "\t" +
                                str(a_p.experience_in_online_shopping) + "\n")

def CreateProfilesFromCopy(path_login, path_user_profile):
    logins = open(path_login).readlines()
    profiles = open(path_user_profile).readlines()
    profiles_dic = {}
    for profile in profiles:
        profile = profile.strip().split("\t")
        profiles_dic[profile[1]] = profile[2:]

    for login in logins:
        login = login.strip().split("\t")
        log = Login.objects.create(user_name = login[1], password=login[2])
        if login[0] in profiles_dic:
            profile = profiles_dic[login[0]]
            print profile
            AssessorProfile.objects.create(login=log.id, career_field=profile[0],
                                       gender=profile[1],
                                       age=profile[2],
                                           experience_in_online_shopping=profile[3])

def Statistics(request):
    #Copy_logins_and_Profiles("static/text_files/logins.txt", "static/text_files/user_profile.txt")
    n_methods = 6
    #CreateProfilesFromCopy("static/text_files/logins.txt", "static/text_files/user_profile.txt")
    tasks = OneTask.objects.all()
    tasks = [task for task in tasks if task.iteration >= 5]
    games_sucsess = [0. for i in range(n_methods)]
    games_fall = [0. for i in range(n_methods)]
    games_length = [0. for i in range(n_methods)]
    for i in tasks:
        spam_game = Game.objects.get(task=i, method_id=5)
        shoe = OneImage.objects.get(id=spam_game.point)
        image = os.path.basename(shoe.image.path)
        if image not in ["8049022.585.jpg", "8122735.594.jpg", "8049088.379012.jpg",
                         "8064935.365347.jpg", "8008094.585.jpg",
                         "8096669.574.jpg", "8101487.7122.jpg",
                         "7804711.1334.jpg", "7448464.12664.jpg", "8036460.36989.jpg"]:
            continue

        game = Game.objects.filter(task=i)
        max_sucsess_iteration = 0
        for g in game:
            if g.sucsess == 1:
                if (g.iteration > max_sucsess_iteration):
                    max_sucsess_iteration = g.iteration
                    print("SUCSEESS ITERATIONS = ", g.iteration)

        print("Normalization = ", max_sucsess_iteration)
        for g in game:
            if g.sucsess == 1:
                games_sucsess[g.method_id] += 1
                games_length[g.method_id] += (float(g.iteration) + 1e-10) / (max_sucsess_iteration + 1e-10)
            if g.sucsess == -1:
                games_fall[g.method_id] += 1
    for i in range(n_methods):
        games_length[i] = float(games_length[i]) / (games_sucsess[i] + 1e-10)
    return render(request, 'final_stage/statistics.html', locals())

def FinalStage(request, game_id, product_id):

    game = Game.objects.get(id=game_id)
    shoe = OneImage.objects.get(id = product_id)

    game.point = product_id
    print("SHOE = ", shoe, game.user_id, game.target_image_id)

    initial_description = ShoeDescriptionByAssessor.objects.get(user_profile=game.user_id,
                                                                image_id=game.target_image_id)
    images = [shoe.image, Shoe.objects.get(id=game.target_image_id).image]
    return render(request, 'final_stage/description_diff.html', locals())

def Description(request, game_id):

    game = Game.objects.get(id=game_id)
    shoe = OneImage.objects.get(id = game.point)

    print("SHOE = ", shoe, game.user_id, game.target_image_id)

    initial_description = ShoeDescriptionByAssessor.objects.filter(user_profile=game.user_id,
                                                                image_id=game.target_image_id)[0]
    images = [shoe.image, Shoe.objects.get(id=game.target_image_id).image]
    return render(request, 'final_stage/description_diff.html', locals())