from django.contrib import admin
from .models import *



class ProductImageInline(admin.TabularInline):
    model = OneImage
    extra = 0


class ImagesInOneLineAdmin (admin.ModelAdmin):
    list_display = [field.name for field in ImagesInOneLine._meta.fields]
    inlines = [ProductImageInline]

    class Meta:
        model = ImagesInOneLine

admin.site.register(ImagesInOneLine, ImagesInOneLineAdmin)


class OneImageAdmin (admin.ModelAdmin):
    list_display = [field.name for field in OneImage._meta.fields]

    class Meta:
        model = OneImage

admin.site.register(OneImage, OneImageAdmin)

class AnswerAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Answer._meta.fields]

    class Meta:
        model = Answer

admin.site.register(Answer, AnswerAdmin)


class OneImageInLine(admin.TabularInline):
    model = OneImage
    extra = 0

class AnswerInLine(admin.TabularInline):
    model = Answer
    extra = 0

class GameAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Game._meta.fields]
    inlines = [OneImageInLine, AnswerInLine]

    class Meta:
        model = Game

admin.site.register(Game, GameAdmin)