from django import forms

from urllib import request
from django.core.files.base import ContentFile
from .models import Image
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,
        }


    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()

        if extension not in valid_extensions:
            raise forms.ValidationError('Image Type Error')

        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False)
        
        # get format url
        image_url = self.cleaned_data['url']
        image_extension = image_url.rsplit('.', 1)[1].lower()
        image_name = '{}.{}'.format(slugify(image.title), image_extension)

        # download and upload
        response = request.urlopen(image_url)
        image_page =  response.read()
        image.image.save(image_name, ContentFile(image_page), save=False)

        if commit:
            image.save()
        return image

