from django.http import HttpResponse
from yaml import safe_load

with open('config.yml', 'r') as config:
    choices = safe_load(config)


def submit(request):
    return HttpResponse()
