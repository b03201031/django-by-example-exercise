from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.shortcuts import reverse

from django.contrib.auth.models import User
# Create your models here.




class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images_created',
                                                       on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d') # as a File instance in model instance
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_liked',
                                                                  blank=True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)
    def __str__(self):
        return self.title

    #override
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, kwargs)


    def get_absolute_url(self):
        return reverse('images:image_detail', args=[self.id, self.slug])



