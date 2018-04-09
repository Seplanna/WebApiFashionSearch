from django.db import models
from landing.models import AssessorProfile


class Shoe(models.Model):
    image = models.ImageField(upload_to='target_products/')
    def __str__(self):
        return "%s" % self.id

class Comfort(models.Model):
    comfort_type = models.CharField(max_length=20, blank=True, null=True, default="Very comfort")

    def __str__(self):
        return "%s" % self.comfort_type

class ShoeDescriptionByAssessor(models.Model):
    user_profile = models.IntegerField(default=0)
    image_id = models.IntegerField(default=0)

    comfort_choises = (
        ("V_C", "very comfort"),
        ("C", "comfort"),
        ("N_C", "not comfort")
    )
    comfort = models.CharField(max_length=3, choices=comfort_choises, default="V_C")

    style = models.CharField(max_length=128, default="-")
    colour = models.CharField(max_length=128, default="-")
    material = models.CharField(max_length=128, default="-")
    brand_name = models.CharField(max_length=128, default="-")
    function = models.CharField(max_length=128, default="-")
    short_description = models.TextField(default="-")

    def __str__(self):
        return "%s" % self.id



