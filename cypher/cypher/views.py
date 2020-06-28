from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from .cyphers import CYPHERS, validate
from .config_loader import resolve_task, get_next_by_hash, COMPLETE_TEXT


def submit(request):
    if request.method != "POST":
        return HttpResponseBadRequest()

    initial = 'ifmmp'
    shift = 1

    if validate(initial, request.POST['answer'], 'Caesar', shift):
        return HttpResponseRedirect('/success')
    else:
        return HttpResponse(content='incorrect')


@require_POST
@resolve_task
def submit_task(request, task):
    if request.body.decode() == task["start"]:
        next_task = get_next_by_hash(task["task"])
        if next_task is None:
            return JsonResponse({"status": "success", "message": COMPLETE_TEXT})
        else:
            return HttpResponseRedirect(f"/view/{next_task['task']}")
    return JsonResponse({"status": "failure", "message": "Incorrect"})


@require_GET
@resolve_task
def task_view(request, task):
    encoder = CYPHERS[task["cypher"]]
    cypher_text = encoder(task["start"], task["key"])
    return render(request, f'{task["cypher"]}.html', {'cypher': cypher_text, "type": task["cypher"]})
