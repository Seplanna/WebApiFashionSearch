from django.contrib import admin
from .models import *


class ShoeInline(admin.TabularInline):
    model = Shoe
    extra = 0


class ShoeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Shoe._meta.fields]

    class Meta:
        model = Shoe

admin.site.register(Shoe, ShoeAdmin)

class ComfortAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comfort._meta.fields]

    class Meta:
        model = Comfort

admin.site.register(Comfort, ComfortAdmin)

class ShoeDescriptionByAssessorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ShoeDescriptionByAssessor._meta.fields]
    class Meta:
        model = ShoeDescriptionByAssessor

admin.site.register(ShoeDescriptionByAssessor, ShoeDescriptionByAssessorAdmin)