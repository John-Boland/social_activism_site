from functools import wraps

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest
from django.views.generic import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def ajax_required(func):
    """A decorator that validates a request is AJAX"""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return func(request, *args, **kwargs)
    return wrapper

class AuthorRequiredMixin(View):
    """Mixin that validiates the logged in user is the creator of the object
    to be edited or updated."""
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)
