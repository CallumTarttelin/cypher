from django.core.exceptions import ValidationError
from hashlib import sha256

from django.http import HttpResponseNotFound
from jsonschema import validate
from yaml import safe_load

from typing import Any, Dict, Iterable, Optional, Tuple, TypeVar

_SCHEMA = {
    "type": "object",
    "properties": {
        "tasks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "cypher": {
                        "type": "string",
                        "enum": ["caesar"]
                    },
                    "start": {
                        "type": "string"
                    },
                    "key": {}
                }
            }
        },
        "complete_text": {
            "type": "string"
        }
    }
    
}
with open('config.yml', 'r') as config:
    _CONFIG = safe_load(config)
T = TypeVar('T')


def with_previous(items: Iterable[T], default=None) -> Iterable[Tuple[T, T]]:
    last = default
    for item in items:
        yield item, last
        last = item


validate(_CONFIG, schema=_SCHEMA)

TASKS = [
    {"task": "" if previous is None else sha256(previous["start"].encode()).hexdigest(), **cypher}
    for cypher, previous in with_previous(_CONFIG["tasks"])
]

COMPLETE_TEXT = _CONFIG["complete_text"]


def get_by_hash(task: str) -> Optional[Dict[str, Any]]:
    if task is None or task == "":
        return TASKS[0]
    tasks = [cfg for cfg in TASKS if cfg["task"] == task]
    if not tasks:
        return None
    if len(tasks) > 1:
        raise IndexError("Too many matching tasks!")
    return tasks[0]


def get_next_by_hash(task: str) -> Optional[Dict[str, Any]]:
    if task is None or task == "":
        return TASKS[1]
    tasks = [i for i, cfg in enumerate(TASKS) if cfg["task"] == task]
    if not tasks or tasks[0] + 1 >= len(TASKS):
        return None
    if len(tasks) > 1:
        raise IndexError("Too many matching tasks!")
    return TASKS[tasks[0] + 1]


def resolve_task(func):
    def inner(request, task_hash="", *args, **kwargs):
        task = get_by_hash(task_hash)
        if task is None:
            return HttpResponseNotFound("Task not found!")
        else:
            return func(request, task, *args, **kwargs)
    return inner
