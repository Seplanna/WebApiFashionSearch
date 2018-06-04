from django.db import models

class InterpretabilityGame(models.Model):
    user_id = models.IntegerField(default=-1)
    target_image = models.CharField(max_length=128,default='')
    question_order = models.CharField(max_length=128,default='')
    iteration = models.IntegerField(default=0)
    game_number = models.IntegerField(default=-1)
    code = models.IntegerField(default=-1)
    def __str__(self):
        return "%s" % (self.id)

class Interpretability(models.Model):
    game_id = models.ForeignKey(InterpretabilityGame, default=1)
    iteration = models.IntegerField(default=-1)
    method_id = models.IntegerField(default=-1)
    feature_n = models.IntegerField(default=-1)
    property_choise = (("T", "type"), ("OC", "occasion"), ("OP", "openness"), ("W", "width"), ("M", "material"),
                       ("H", "heel"), ("C", "color"), ("La", "Laces"), )
    property = models.CharField(max_length=3, default='', choices=property_choise)
    how_obvious_it_is = models.IntegerField(default=-1)
