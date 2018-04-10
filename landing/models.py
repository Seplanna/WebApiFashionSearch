from django.db import models


#class Subscriber(models.Model):
#    email = models.EmailField()
#    name = models.CharField(max_length=128)
#
#    def __str__(self):
#        return "User %s %s" % (self.name, self.email,)
#
#    class Meta:
#        verbose_name = 'MySubscriber'
#        verbose_name_plural = 'A lot of Subscribers'

class Gender(models.Model):
    gender = models.CharField(max_length=20, blank=True, null=True, default=None)
    def __str__(self):
        return "%s" % self.gender

class AssessorProfile(models.Model):

    gender_choises=(
        ("W", "woman"),
        ("M", "man"),
        ("O", "prefer not to tell")
    )
    gender = models.CharField(max_length=1, choices=gender_choises)

    age_choices = (
        ("0", "less than 18"),
        ("1", "18-23"),
        ("2", "23-27"),
        ("3", "27-35"),
        ("4", "older than 35")
    )
    age = models.CharField(max_length=1, choices=age_choices)

    carrer_feild_choices = (
        ("1", "Computers and Technology"),
        ("2", "Health Care and Allied Health"),
        ("3", "Education and Social Services"),
        ("4", "Arts and Communications"),
        ("5", "Trades and Transportation"),
        ("6", "Management, Business, and Finance"),
        ("7", "Architecture and Civil Engineering"),
        ("8", "Science"),
        ("9", "Hospitality, Tourism, and the Service Industry"),
        ("10", "Law and Law Enforcement"),
        ("11", "other"))
    carrer_feild = models.CharField(max_length=2, choices=carrer_feild_choices)

    online_shop_expirience_choises = (
        ("0", "I am mostly shopping online(make purchases every month)"),
        ("1", "I do online shopping once or twice per year"),
        ("2", "Have never done it"))

    expirience_in_online_shopping = models.CharField(max_length=40,
                                              choices=online_shop_expirience_choises)

    def __str__(self):
        return str(self.id)