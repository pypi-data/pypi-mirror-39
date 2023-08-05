from django.http import JsonResponse
from python_utils import converters

from . import null_to_emtpy


def param(request, key, default=None):
    if isinstance(key, list):
        return [param(request, item, default) for item in key]
    value = request.GET.get(key)
    if value is None:
        value = request.POST.get(key)
    if value is None:
        value = default
    return value


def int_param(request, param_name, default=0):
    return converters.to_int(param(request, param_name), default)


def bool_param(request, param_name ):
    value = param(request, param_name, "")
    return value.upper() in ["TRUE", "1", "OK"]


def json_response(dict_instance: dict):
    return JsonResponse(null_to_emtpy(dict_instance))
