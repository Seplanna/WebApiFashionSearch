from django.contrib import admin
from .models import *


class InterpretabilityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Interpretability._meta.fields]
    class Meta:
        model = Interpretability

admin.site.register(Interpretability, InterpretabilityAdmin)


class InterpretabilityInLine(admin.TabularInline):
    model = Interpretability
    extra = 0

class InterpretabilityGameAdmin(admin.ModelAdmin):
    list_display = [field.name for field in InterpretabilityGame._meta.fields]
    inlines = [InterpretabilityInLine]

    class Meta:
        model = InterpretabilityGame

admin.site.register(InterpretabilityGame, InterpretabilityGameAdmin)


