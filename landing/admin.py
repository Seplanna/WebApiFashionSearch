from django.contrib import admin
from .models import *

class GenderAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Gender._meta.fields]
    class Meta:
        model = Gender

admin.site.register(Gender, GenderAdmin)


class AssessorProfileAdmin (admin.ModelAdmin):
    # list_display = ["name", "email"]
    list_display = [field.name for field in AssessorProfile._meta.fields]
    class Meta:
        model = AssessorProfile

admin.site.register(AssessorProfile, AssessorProfileAdmin)

"""class SubscriberAdmin (admin.ModelAdmin):
    # list_display = ["name", "email"]
    list_display = [field.name for field in Subscriber._meta.fields]
    list_filter = ['name',]
    search_fields = ['name', 'email']

    fields = ["email"]

    # exclude = ["email"]
	# inlines = [FieldMappingInline]
	# fields = []
    # #exclude = ["type"]
	# #list_filter = ('report_data',)
	# search_fields = ['category', 'subCategory', 'suggestKeyword']

    class Meta:
        model = Subscriber

admin.site.register(Subscriber, SubscriberAdmin)"""