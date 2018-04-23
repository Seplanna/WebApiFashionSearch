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
    CreateProfilesFromCopy("static/text_files/logins.txt", "static/text_files/user_profile.txt")
    tasks = OneTask.objects.all()
    tasks = [task for task in tasks if task.iteration >= 5]
    games_sucsess = [0. for i in range(n_methods)]
    games_fall = [0. for i in range(n_methods)]
    for i in tasks:
        game = Game.objects.filter(task=i)
        for g in game:
            if g.sucsess == 1:
                games_sucsess[g.method_id] += 1
            if g.sucsess == -1:
                games_fall[g.method_id] += 1
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