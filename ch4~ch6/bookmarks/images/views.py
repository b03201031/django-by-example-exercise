from django.shortcuts import render, redirect, get_object_or_404

from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ImageCreateForm
from .models import Image


# Create your views here.

@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')

    print(image_id)
    print(action)

    if image_id and action:
        try:
           
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                print('called')
                image.users_like.remove(request.user)

            DATA = {
                'status': 'ok',
            }

            return JsonResponse(DATA)

        except:
            pass
    
    
    DATA = {
        'status': 'ko'
    }
    return JsonResponse(DATA)

def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)

    TEMPLATE_PATH = 'images/image/detail.html'
    CONTEXT = {
        'section': 'images',
        'image': image,
    }

    return render(request, TEMPLATE_PATH, context=CONTEXT)


@login_required
def image_create(request):
    if request.method == 'POST':
        create_form = ImageCreateForm(data=request.POST)

        if create_form.is_valid():
            new_image = create_form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            messages.success(request, 'Image successfully add')

            return redirect(new_image.get_absolute_url())
    else:
        create_form = ImageCreateForm(data=request.GET)


    TEMPLATE_PATH = 'images/image/create.html'
    CONTEXT = {
        'section': 'images',
        'create_form': create_form,
    }

    return render(request, TEMPLATE_PATH, context=CONTEXT)