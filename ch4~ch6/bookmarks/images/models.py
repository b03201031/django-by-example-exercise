from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.shortcuts import reverse

from django.contrib.auth.models import User
# Create your models here.

class Contact(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_from_set',
                                                           on_delete='CASCADE')
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_to_set',
                                                         on_delete='CASCADE')
    created = models.DateField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)

#monkey patch
# 使用中间表格作为多对多关系的中间表时，一些管理器的内置方法如add()，create()，remove()等无法使用，必须编写直接操作中间表的代码。
User.add_to_class('following',
                   models.ManyToManyField('self', through=Contact,
                                                  through_fields=('user_from', 'user_to'),
                                                  related_name='followers',
                                                  symmetrical=False))

class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images_created',
                                                       on_delete='CASCADE')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d') # as a File instance in model instance
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_liked',
                                                                  blank=True)

    def __str__(self):
        return self.title

    #override
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, kwargs)


    def get_absolute_url(self):
        return reverse('images:image_detail', args=[self.id, self.slug])



