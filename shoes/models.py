from django.db import models
from landing.models import AssessorProfile


class Shoe(models.Model):
    image = models.ImageField(upload_to='target_products/')
    def __str__(self):
        return "%s" % self.id

class ShoeDescriptionByAssessor(models.Model):
    user_profile = models.IntegerField(default=0)
    image_id = models.IntegerField(default=0)
    #comfort = models.CharField(max_length=128, default="")
    #style = models.CharField(max_length=128, default="")
    #colour = models.CharField(max_length=128, default="")
    #material = models.CharField(max_length=128, default="")
    #brand_name = models.CharField(max_length=128, default="")
    #function = models.CharField(max_length=128, default="")
    short_description = models.TextField(default="")
    choises_buy_for_yourself=(("Y", "yes"), ("N", "no"))
    will_you_buy_it_for_your_self = models.CharField(max_length=3, choices=choises_buy_for_yourself)

    def __str__(self):
        return "%s" % self.id



