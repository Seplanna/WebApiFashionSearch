from django.db import models
from shoes.models import Shoe, ShoeDescriptionByAssessor, OneTask




class Game(models.Model):
    user_id = models.IntegerField(default=-1)
    method_id = models.IntegerField(default=-1)
    target_image_id = models.IntegerField(default=-1)
    task = models.ForeignKey(OneTask)

    sucsess = models.IntegerField(default=0)
    feature_n = models.IntegerField(default=0)
    point = models.IntegerField(default=-1)
    data = models.TextField(default="")
    point_features = models.TextField(default="")
    iteration = models.IntegerField(default=0)
    change_data = models.BooleanField(default=False)


    def __str__(self):
        return "%s" % (self.id)

class Interpretability(models.Model):
    game_id = models.ForeignKey(Game, default=1)
    iteration = models.IntegerField(default=-1)
    property = models.CharField(max_length=128, default='')
    how_obvious_it_is = models.IntegerField(default=-1)

class Answer(models.Model):
    iteration = models.IntegerField(default=-1)
    feature_n = models.IntegerField(default=0)
    answer = models.IntegerField(default=-1)
    game_id = models.ForeignKey(Game, default=1)

class ImagesInOneLine(models.Model):
    line_number = models.IntegerField(default=-1)
    def __str__(self):
        return "%s" % self.id

class OneImage(models.Model):
    line_id = models.ForeignKey(ImagesInOneLine, default=1)
    game_id = models.ForeignKey(Game, default=1)
    image = models.ImageField(upload_to='product/ut-zap50k-images/')
    def __str__(self):
        return "%s_%s" % (self.id,self.line_id.id)


class Feedback(models.Model):
    feedback = models.TextField()
    task_id = models.IntegerField()
    def __str__(self):
        return "%s" % self.id
