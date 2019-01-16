from django.http import HttpResponseBadRequest
from functools import wraps


def ajax_required(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        else:
            return f(request, *args, **kwargs)

    return wraps