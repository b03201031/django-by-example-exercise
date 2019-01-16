from django.shortcuts import render

# Create your views here.
@login_required
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.value_list('id', flat=True)

    if following_ids:
        actoin = action.objects.filter(user_id__in=following_ids)
    actions = actions[:10]
    TEMPLATE_PATH = 'account/dashboard.html'
    CONTEXT = {
        'section': 'dashboard',
        'actions': actions,
    }
    return render(request, TEMPLATE_PATH, context=CONTEXT)