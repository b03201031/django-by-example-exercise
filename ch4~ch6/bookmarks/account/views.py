from django.shortcuts import render, HttpResponse
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# Create your views here.

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


