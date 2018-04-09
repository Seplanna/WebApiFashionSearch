from django.shortcuts import render, HttpResponseRedirect
from .forms import OneImage, Game, Shoe, ShoeDescriptionByAssessor
import os
import numpy as np
#from products.models import *


def FinalStage(request, game_id, product_id):

    game = Game.objects.get(id=game_id)
    shoe = OneImage.objects.get(id = product_id)

    game.point = product_id
    print("SHOE = ", shoe, game.user_id, game.target_image_id)

    initial_description = ShoeDescriptionByAssessor.objects.get(user_profile=game.user_id,
                                                                image_id=game.target_image_id)
    images = [shoe.image, Shoe.objects.get(id=game.target_image_id).image]
    return render(request, 'final_stage/description_diff.html', locals())

def Description(request, game_id, product_id):

    game = Game.objects.get(id=game_id)
    shoe = OneImage.objects.get(id = product_id)

    game.point = product_id
    print("SHOE = ", shoe, game.user_id, game.target_image_id)

    initial_description = ShoeDescriptionByAssessor.objects.get(user_profile=game.user_id,
                                                                image_id=game.target_image_id)
    images = [shoe.image, Shoe.objects.get(id=game.target_image_id).image]
    return render(request, 'final_stage/description_diff.html', locals())