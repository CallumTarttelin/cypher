from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from yaml import safe_load

from .cyphers import validate

with open('config.yml', 'r') as config:
    choices = safe_load(config)


def submit(request):
    if request.method != "POST":
        return HttpResponseBadRequest()

    initial = 'ifmmp'
    shift = 1

    if validate(initial, request.POST['answer'], 'Caesar', shift):
        return HttpResponseRedirect('/success')
    else:
        return HttpResponse(content='incorrect')
