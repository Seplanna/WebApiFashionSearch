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

class InterpretabilityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Interpretability._meta.fields]
    class Meta:
        model = Interpretability

admin.site.register(Interpretability, InterpretabilityAdmin)

class OneImageInLine(admin.TabularInline):
    model = OneImage
    extra = 0

class AnswerInLine(admin.TabularInline):
    model = Answer
    extra = 0

class InterpretabilityInLine(admin.TabularInline):
    model = Interpretability
    extra = 0

class GameAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Game._meta.fields]
    inlines = [OneImageInLine, AnswerInLine, InterpretabilityInLine]

    class Meta:
        model = Game

admin.site.register(Game, GameAdmin)

class GameInLine(admin.TabularInline):
    model=Game
    extra=0

class TaskAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OneTask._meta.fields]
    inlines = [GameInLine]

    class Meta:
        model = OneTask

admin.site.register(OneTask, TaskAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    model=Feedback
    extra=0

admin.site.register(Feedback, FeedbackAdmin)

