from django.contrib import admin
from .models import *

class AssessorProfileAdmin (admin.ModelAdmin):
    # list_display = ["name", "email"]
    list_display = [field.name for field in AssessorProfile._meta.fields]
    class Meta:
        model = AssessorProfile

admin.site.register(AssessorProfile, AssessorProfileAdmin)

class  LoginFormAdmin (admin.ModelAdmin):
    #list_display = ["user_name", "password"]
    list_display = [field.name for field in  Login._meta.fields]
    class Meta:
        model =  Login

admin.site.register( Login,  LoginFormAdmin)
