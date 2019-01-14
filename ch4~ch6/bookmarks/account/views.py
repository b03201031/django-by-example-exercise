from django.shortcuts import render, HttpResponse
from .forms import LoginForm, userRegistrationForm
from .forms import UserEditForm, ProfileEditForm

from .models import Profile

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, 
                                       data=request.POST,
                                       files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Profile updated successfully')
        
        else:
            messages.error(request, 'Error updating yout profile')

    try:
        Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        Profile.objects.create(user=request.user)

    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)


    TEMPLATE_PATH = 'account/edit.html'
    
    CONTEXT = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, TEMPLATE_PATH, context=CONTEXT)

def register(request):
    if request.method == 'POST':
        register_form = userRegistrationForm(data=request.POST)

        if register_form.is_valid():

            cd = register_form.cleaned_data
            new_user = register_form.save(commit=False)
            new_user.set_password(cd['password'])
            new_user.save()

            Profile.objects.create(user=new_user)
            
            context = {
                'new_user': new_user,
            }
            TEMPLATE_PATH = 'account/register_done.html'

            return render(request, TEMPLATE_PATH, context=context)
    else:
        register_form = userRegistrationForm()
        
        TEMPLATE_PATH = 'account/register.html'
        context = {
            'register_form': register_form,
        }
        return render(request, TEMPLATE_PATH, context=context)

@login_required
def dashboard(request):
    TEMPLATE_PATH = 'account/dashboard.html'
    context = {
        'section': 'dashboard'
    }
    return render(request, TEMPLATE_PATH, context=context)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
             
        if form.is_valid():
            print('vallid')
            # return True
            # place form's data in cleaned_data
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'],
                                         password=cd['password'])
            print(user)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authenticated successfully")

                else:
                    return HttpResponse("Disabled account")

            else:
                return HttpResponse("Invalid login")

        print('not')
    else:
        form = LoginForm()

    TEMPLATE_PATH = 'account/login.html'

    context = {
        'form': form,
    }
    
    return render(request, TEMPLATE_PATH, context=context)


