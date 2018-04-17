from django.shortcuts import render, HttpResponseRedirect
from .forms import ImagesInOneLine, OneImage, Game, Answer, ShoeDescriptionByAssessorForm, \
    Shoe, ShoeDescriptionByAssessor, AnswerForm, OneTask
from shoes.views import TakeImageIdFromTask, ChooseTask
import os
import numpy as np
import random

n_bins = 5
n_pictures_per_bin = 5
n_features = 5
n_methods = 5
#from products.models import *

#----------------------delete-----------------------------------------------
def GetMedian(features_in_bins):
    features_in_bins = np.array(features_in_bins)
    median = np.median(features_in_bins, axis=0)
    return median


def RecieveBinOfTheFeature(value, bins, n_bins):
    bin = 0
    while (bin < n_bins - 1 and value > (bins[bin])):
        bin += 1
    if (bin == n_bins):
        bin -= 1
    return bin

def DevideFeatureIntoBinsFromData(values, n_bins):

    arg_sort = np.argsort(values)
    step = len(values) / n_bins
    values = np.array(values)
    bins = values[arg_sort[0::step]]
    bins = bins[1:]
    last_value = bins[0]
    return bins

def ReturnImagesCLosedToMedian(features_in_bins, data_by_bins, n_bins, n_pictures_per_bin, median):
    features_in_bins = np.array(features_in_bins)
    closest_to_median_images = [[] for i in range(n_bins)]
    for bin in range(n_bins):
        print("BIN = ", bin)
        feature_in_bin = features_in_bins[data_by_bins[bin]]
        feature_in_bin -= median
        norms = np.linalg.norm(feature_in_bin, axis=1)
        argsort = np.argsort(norms)
        n_pictures_per_bin_ = n_pictures_per_bin
        print(norms[argsort[0]], bin)
        if (n_pictures_per_bin < 0):
            n_pictures_per_bin_ = len(data_by_bins[bin])
        for i in range(n_pictures_per_bin_):
            closest_to_median_images[bin].append(data_by_bins[bin][argsort[i]])
    return closest_to_median_images



def  Real1_one_feature_from_given_features(features, data_len, n_bins, n_pictures_per_bin, feature_n, point_features,
                                           point=-1
                                           ):
    features_in_bins = []
    feature_values = []
    for d in range(len(data_len)):
        features_= np.array(features[d])
        feature_value = features_[feature_n]
        feature_values.append(feature_value)
        features_ = [features_[f] for f in range(features_.shape[0]) if f != feature_n]
        features_in_bins.append(features_)

    bins = DevideFeatureIntoBinsFromData(feature_values, n_bins)
    print("BINS VALUES = ", bins)

    data_by_bins = [[] for i in range(n_bins)]

    for d in range(len(feature_values)):
        bin = RecieveBinOfTheFeature(feature_values[d], bins, n_bins)
        data_by_bins[bin].append(d)
#--------------------------For the situation when value of some bins is equal---------------------
    first_bin = 0
    last_bin = 0
    while last_bin < len(data_by_bins):
        if len(data_by_bins[last_bin]) > 0:
            if (last_bin - first_bin == 0):
                last_bin += 1
                first_bin = last_bin
            else:
                n_splits = last_bin - first_bin + 1
                elements = data_by_bins[last_bin]
                random.shuffle(elements)
                step = len(elements) / n_splits
                for bin_ in range(last_bin - first_bin):
                    data_by_bins[first_bin + bin_] = elements[step * bin_: step * (bin_ + 1)]
                data_by_bins[last_bin] = elements[step * (bin_ + 1):]
                last_bin += 1
                first_bin = last_bin
        else:
            last_bin += 1
# --------------------------For the situation when value of some bins is equal---------------------


    print("POINT =", point)
    if point < 0:
        median = GetMedian(features_in_bins)
    else:
        print("AAAA POINT > 0")
        features_ = np.array([float(f) for f in point_features.split("_")[:-1]])
        median = [features_[f] for f in range(features_.shape[0]) if f != feature_n]
        print(median)
    return ReturnImagesCLosedToMedian(features_in_bins, data_by_bins,  n_bins, n_pictures_per_bin, median), data_by_bins
#----------------------end delete-------------------------------------------
def CreateCatolog(n_bins, data_path):
    lines = []
    for l in range(n_bins+1):
        lines.append(ImagesInOneLine.objects.create(line_number=(l-1)))

    """data = []
    for root, subdirs, files in os.walk(data_path):
        for f in files:
            if os.path.splitext(f)[1].lower() in ('.jpg', '.jpeg'):
                data += [os.path.join(root, f)]
    print(len(data))
    for d in data:
        d_ = "/".join((d.split("/")[2:]))
        print(d_)
        OneImage.objects.create(image=d_)"""
#-----------------------------------------------------------------------------
def GetFeturesFromText(text):
    data = text.split("\n")[:-1]
    features = []
    for d in data:
        d1 = d.split("_")[:-1]
        features.append([float(f) for f in d1])
    return np.array(features), data

def GetFeaturesForOneImage(image_url, data):
    data1 = data.strip().split("\n")
    for d in range(len(data1)):
        if data1[d].split("_")[-1] == image_url:
            return data1[d]

def GangeLineIdsInImages(images_in_lines, game, data):
    lines = [line for line in ImagesInOneLine.objects.all() if line.line_number >= 0]
    imgs = []
    for l in lines:
        imgs += OneImage.objects.filter(game_id=game, line_id=l)
    print("LEN_IMAGES = ", len(imgs))
    #for m in imgs:
    #    m.line_id = line
    #    m.save()
    img_ind = 0
    for bin in range(len(images_in_lines)):
        line = ImagesInOneLine.objects.filter(line_number=bin)[0]

        for im_n in images_in_lines[bin]:
            im_url = "product/" + data[im_n].split("_")[-1]
            img = imgs[img_ind]
            img.line_id = line
            img.image = im_url
            img.save()
            img_ind += 1


def GhangeTheOrderOfTheImages(ims, lines):
    print("START = ", ims)
    for i in ims:
        if i.line_id.line_number == 0:
            i.line_id = lines[1]
            i.save()
        elif i.line_id.line_number == 1:
            i.line_id = lines[0]
            i.save()
    print("END = ", ims)

def TakeDatasetFromMethodNumber(number):
    mehtods = {0:"static/text_files/My.csv",
               1:"static/text_files/ClusterDirection.csv",
               2: "static/text_files/InfoGAN.csv",
               3: "static/text_files/PCA_AutoEncoder.csv",
               4: "static/text_files/PCA_GIST.csv",
               }
    return mehtods[number]

def CreateGame(user_id, task):
    target_image_id = TakeImageIdFromTask(task)
    method_id = int(task.methods.strip().split("\t")[task.iteration])
    if Game.objects.filter(user_id=user_id, target_image_id=target_image_id, method_id=method_id,
                               task=task).exists():
        Game.objects.filter(user_id=user_id, target_image_id=target_image_id, method_id=method_id,
                               task=task).delete()

    if not Game.objects.filter(user_id=user_id, target_image_id=target_image_id, method_id=method_id,
                               task=task).exists():
        data_path = TakeDatasetFromMethodNumber(method_id)
        with open(data_path, 'r') as data_:
            data = data_.read()
        game = Game.objects.create(user_id=user_id, target_image_id=target_image_id, method_id=method_id,
                                   data=data, task=task)
        lines = [line for line in ImagesInOneLine.objects.all() if line.line_number >= 0]

        data_path_ = "static/media/product/"
        data = []
        for root, subdirs, files in os.walk(data_path_):
            for f in files:
                if os.path.splitext(f)[1].lower() in ('.jpg', '.jpeg'):
                    data += [os.path.join(root, f)]

        for line in lines:
            for im in range(n_pictures_per_bin):
                d_ = random.choice(data)
                d_ = "/".join((d_.split("/")[2:]))
                OneImage.objects.create(game_id=game, line_id=line, image=d_)

def ChangeAnswer(answer, answer_, data, data_in_bins):
    print("ANSWER")
    game = answer.game_id
    if answer.status == "color":
        answer.colour_answer = answer_
        answer.status = "shape"
        answer.save()
        #return HttpResponseRedirect("/search/" + str(game.id) + "/")
    elif answer.status == "shape":
        answer.shape_answer = answer_
        answer.status = "best image"
        answer.save()

        game = answer.game_id
        if (answer.colour_answer >= 0 and answer.shape_answer >= 0):
            if (answer.colour_answer != answer.shape_answer):
                return HttpResponseRedirect("/best_picture/" + str(game.id) + "/")
        if (answer.colour_answer < 0 and answer.shape_answer < 0):
            return HttpResponseRedirect("/best_picture/" + str(game.id) + "/")

        game.feature_n += 1
        game.iteration += 1
        game.save()
        line = max(answer.colour_answer, answer.shape_answer)
        data = [data[i] for i in data_in_bins[line]]
        game.data = "\n".join(data)
        game.save()
        return HttpResponseRedirect("/search/" + str(game.id) + "/")

    else:
        answer.best_image_id = answer_
        answer.save()
        game = answer.game_id
        game.iteration += 1
        #if (answer_ < 0):
        game.feature_n += 1
        if answer_ >= 0:
            image = OneImage.objects.get(id=answer_)
            game.point_features = GetFeaturesForOneImage(image.image.url.split("/")[-1], game.data)
            game.point = answer_
        game.save()
        print(game.point_features, game.point, game.id)
        return HttpResponseRedirect("/search/"+ str(game.id) + "/")

def Get_data_data_in_bins_answer(game_id, n_bins, n_pictures_per_bin, n_features):
    game = Game.objects.filter(id=game_id)[0]

    if not Answer.objects.filter(game_id=game, iteration=game.iteration).exists():
        Answer.objects.create(game_id=game, iteration=game.iteration)
    answer = Answer.objects.filter(game_id=game, iteration=game.iteration)[0]

    features,data = GetFeturesFromText(game.data)
    print(features.shape)

    images_in_bins, data_in_bins = \
        Real1_one_feature_from_given_features(features,
                                              data,
                                              n_bins,
                                              n_pictures_per_bin,
                                              game.feature_n % n_features,
                                              game.point_features,
                                              game.point)
    GangeLineIdsInImages(images_in_bins, game, data)
    lines = [line for line in ImagesInOneLine.objects.all() if line.line_number >= 0]

    print("Feature number ", game.feature_n)
    print(features.shape)

    return data, data_in_bins, answer, lines, images_in_bins



def FinishIfNotEnoughImages(game_id, n_bins, n_pictures_per_bin):
    data = Game.objects.filter(id=game_id)[0].data
    data = data.strip().split("\n")
    if len(data) < n_bins * n_pictures_per_bin:
        return True
    return  False


def SpamQuestionCreate(game_id):
    game = Game.objects.get(id=game_id)
    task = game.task
    images = task.images.strip().split("\t")

    spams = [line for line in open("static/text_files/spam.txt").readlines() if
             len(line.strip().split("\t")) > 0 and line.strip().split("\t")[-1] in images]

    lines = [line for line in ImagesInOneLine.objects.all() if line.line_number >= 0]
    imgs = []
    for l in lines:
        imgs += OneImage.objects.filter(game_id=game, line_id=l)

    ind = 0
    for image in images:
        for spam in spams:
            if spam.strip().split("\t")[-1] == image:
                print("SPAM DETECTOR = ", image, spam)
                spam = spam.strip().split("\t")[n_pictures_per_bin*(game.iteration / 5):
                n_pictures_per_bin * (game.iteration / 5 + 1)]
                for im in spam:
                    imgs[ind].image = "/product/" + im
                    imgs[ind].save()
                    ind += 1
    return task.iteration





def SearchSessionEnd(request, game_id):
    game = Game.objects.get(id=game_id)
    task = game.task
    task.iteration += 1
    task.save()
    products = Shoe.objects.all()
    user_id = game.user_id
    n_search_sessions = len(Game.objects.filter(user_id=game.user_id))
    task_id = task.id
    finished_5 = n_search_sessions%5==0
    if (finished_5):
        task = ChooseTask(game.user_id)
        task_id = task.id
    return render(request, 'search/end_session.html', locals())

def Description(request, game_id, product_id):
    chosen_shoe_description = True
    title = "Step 5: Describe the difference"
    end_game_description = True
    game = Game.objects.get(id=game_id)
    shoe = OneImage.objects.get(id = product_id)

    game.point = product_id
    print("SHOE = ", shoe, game.user_id, game.target_image_id)

    form = ShoeDescriptionByAssessorForm(request.POST or None)

    initial_description = ShoeDescriptionByAssessor.objects.filter(user_profile=game.user_id,
                                                                image_id=game.target_image_id)[0]
    images = [shoe.image, Shoe.objects.get(id=game.target_image_id).image]

    form["short_description"].initial = initial_description.short_description
    form["will_you_buy_it_for_your_self"].initial = initial_description.will_you_buy_it_for_your_self


    print("form is valid = ", form.is_valid())
    if request.method == "POST" and form.is_valid():
        print(form.cleaned_data)
        new_form = form.save(commit=False)
        new_form.image_id = product_id
        new_form.user_profile = game.user_id
        new_form.save()
        return HttpResponseRedirect("/search_session_end/" + str(game.id) + "/")
    #return render(request, 'search/description_best_picture.html', locals())
    return render(request, 'products/description_the_picture.html', locals())

def Will_you_buy(request, game_id, product_id):
    game = Game.objects.get(id=game_id)
    shoe = OneImage.objects.get(id=product_id)
    if request.GET.get('BUY') == "yes!":
        game.sucsess = 1
        game.save()
        return HttpResponseRedirect("/description_best_image/"+ str(game_id) + "/" + str(product_id) + "/")
    if request.GET.get('BUY') == "no!":
        game.sucsess = -1
        game.save()
        return HttpResponseRedirect("/description_best_image/" + str(game_id) + "/" + str(product_id) + "/")
    return render(request, 'search/will_you_buy.html', locals())

def Finish(request, game_id):
    skip = False
    game = Game.objects.get(id=game_id)
    data = Game.objects.filter(id=game_id)[0].data
    data = data.strip().split("\n")
    game_notsucseess = (game.sucsess == -1)

    imgs_ = OneImage.objects.filter(game_id=game)
    imgs = []
    ims = []
    for d in range(len(data)):

        d_ = "product/" + data[d].split("_")[-1]
        ims.append(imgs_[d])
        ims[-1].image = d_
        ims[-1].save()
        if len(ims) % n_pictures_per_bin == 0 or d == len(data)-1:
            imgs.append(ims)
            ims = []

    print("IMGS = ", imgs)
    try:
        answer_ = int(request.GET.get('NEXT'))
        game.point = answer_
        game.save()

        if not game.sucsess == 0:
            return HttpResponseRedirect("/description_best_image/"+ str(game_id) + "/" + str(answer_) + "/")
        else:
            return HttpResponseRedirect("/will_you_buy/" + str(game_id) + "/" + str(answer_) + "/")


    except:
        print(request.GET.get('NEXT'))
    return render(request, 'search/best_picture.html', locals())

def ChoseTheBestPicture(request, game_id):
    #user_id = USER_ID
    skip = True

    data, data_in_bins, answer, lines, images_in_bins = Get_data_data_in_bins_answer(game_id, n_bins, n_pictures_per_bin, n_features)
    imgs = []
    for line in lines:
        imgs.append(OneImage.objects.filter(line_id=line, game_id=Game.objects.get(id=game_id)))

    if request.GET.get('NEXT') == "SKIP":
        return ChangeAnswer(answer, -1, data, data_in_bins)
    try:
        answer_ = int(request.GET.get('NEXT'))
        return ChangeAnswer(answer, answer_, data, data_in_bins)


    except:
        print(request.GET.get('NEXT'))
    return render(request, 'search/best_picture.html', locals())



def landing(request, game_id):
    print("START")
    url = "/search/"
    buy_button = True

    game = Game.objects.filter(id=game_id)[0]
    if FinishIfNotEnoughImages(game_id, n_bins, n_pictures_per_bin):
        return HttpResponseRedirect("/finish/" + str(game.id) + "/")

    if game.iteration%5==0 and game.iteration / 5 < 3:
    #--------------------------spam_detector-------------------------------------------
        buy_button = False
        if not Answer.objects.filter(game_id=game, iteration=game.iteration).exists():
            Answer.objects.create(game_id=game, iteration=game.iteration)
        answer = Answer.objects.filter(game_id=game, iteration=game.iteration)[0]
        answer.best_image_id = -SpamQuestionCreate(game_id)
        imgs = []
        for i in range(n_bins):
            line = ImagesInOneLine.objects.get(line_number=i)
            imgs.append(OneImage.objects.filter(game_id=game, line_id=line))

        form = AnswerForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                final_score = form.cleaned_data['Answer_color']
                answer.colour_answer = int(final_score)
                answer.save()
                final_score = form.cleaned_data['Answer_shape']
                answer.shape_answer = int(final_score)
                answer.save()

                print (answer.status, answer.colour_answer)
                game.iteration += 1
                game.save()
                return HttpResponseRedirect("/search/" + str(game.id) + "/")
    # --------------------------spam_detector-------------------------------------------

    else:
        data, data_in_bins, answer, lines, images_in_bins = \
            Get_data_data_in_bins_answer(game.id, n_bins, n_pictures_per_bin, n_features)


        imgs = []
        for i in range(n_bins):
            line = ImagesInOneLine.objects.get(line_number=i)
            imgs.append(OneImage.objects.filter(game_id=game, line_id=line))

        values = range(n_bins)
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()

        if request.GET.get('BUY') == '1' or request.GET.get('FINISH') == '1':
            game = Game.objects.filter(id=game_id)[0]
            game.sucsess = -1
            if (request.GET.get('BUY') == '1'):
                game.sucsess = 1

            data1 = ""
            for bin in images_in_bins:
                for im in bin:
                    data1 += data[im] + "\n"
            game.data = data1
            game.save()
            return HttpResponseRedirect("/finish/" + str(game.id) + "/")

        form = AnswerForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                final_score = form.cleaned_data['Answer_color']
                answer.colour_answer = int(final_score)
                answer.status = "shape"
                answer.save()
                final_score = form.cleaned_data['Answer_shape']
                print (answer.status, answer.colour_answer)
                return ChangeAnswer(answer, int(final_score), data, data_in_bins)


    return render(request, 'search/search.html', locals())


def SearchSessionStart(request, user_id, task_id):
    if not ImagesInOneLine.objects.exists():
        CreateCatolog(n_bins, "static/media/product/")
    #method_id = random.randint(0, n_methods-1)
    task = OneTask.objects.get(id=task_id)
    CreateGame(user_id, task)
    target_image_id = TakeImageIdFromTask(task)
    method_id = int(task.methods.strip().split("\t")[task.iteration])
    game = Game.objects.filter(user_id=user_id, target_image_id=target_image_id, method_id=method_id,
                               task=task)[0]
    game_id = game.id
    return render(request, 'search/start_search.html', locals())
