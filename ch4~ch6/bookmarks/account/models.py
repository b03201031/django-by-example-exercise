from django.db import models
from django.conf import settings

# Create your models here.
# blank for form
# null for db i.e. set blank field to be bull 
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete='CASCADE')
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user/%Y/%m/%d', blank=True)

    def __str__(self):
        return "Profile for user {}".format(self.user.username)