import json
from functools import wraps
from inspect import isfunction

from django.conf import settings
from django.http import HttpResponse
from django.urls import path as django_patb
from django.views.decorators.csrf import csrf_exempt

from acmin.utils import *

methods = {}


def get_urlpatterns():
    return [
        django_patb(r, get_view(func), name=f"{func.__module__}.{func.__qualname__}")
        for r, func in methods.items()
    ]


def admin_route(path):
    from django.conf import settings
    return route(path, f"{settings.ACMIN_ADMIN_PREFIX}/{settings.ACMIN_APP_NAME}" or "")


def route(path, prefix=""):
    def decorate(func):
        new_path = prefix + path
        if new_path.startswith("/"):
            new_path = new_path[1:]
        methods[new_path] = func

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorate


def get_view(func):
    qualname = func.__qualname__
    module_name = func.__module__
    cls = None
    if "." in qualname:
        class_name, _ = qualname.split(".")
        cls = import_class("%s.%s" % (module_name, class_name))

        @csrf_exempt
        def view(request, *args, **kwargs):
            obj = cls()
            obj.request = request
            obj.args = args
            obj.kwargs = kwargs
            return func(obj, *args, **kwargs)
    else:
        def view(request, *args, **kwargs):
            return func(request, *args, **kwargs)

    return view


class Result(object):
    def __init__(self, status=1, data=None):
        self.status = status
        self.data = data


def to_json(data, fields):
    if 'QuerySet' in str(type(data)):
        result = [to_json(obj, fields) for obj in data]
    else:
        result = {}
        for name in fields:
            field = name
            if "|" in name:
                parts = name.split("|")
                name = parts[1]
                field = parts[0] + ".id"
            result[name] = attrs.attr(data, field)
    return result


class RouteMeta(type):
    def __new__(mcs, name, bases, attrs):
        cls = type.__new__(mcs, name, bases, attrs)

        for key, value in attrs.items():
            if isfunction(value):
                u = attr(value, "url")
                if u:
                    app_name = cls.__module__.split(".")[0]
                    prefix = f'/{cls._function_name}/{app_name}/{cls.__module__.split(".").pop()}'
                    setattr(cls, key, route(u, prefix)(value))

        return cls


class AcminView(metaclass=RouteMeta):

    def context(self):
        return {}

    def render(self, template_name: str, context: dict = None):
        updated_context = self.context() or {}
        updated_context.update(context or {})
        name = template_name[1:] if template_name.startswith("/") else template_name
        return render(self.request, name, updated_context)

    @staticmethod
    def json_response(dict_instance: dict):
        return json_response(dict_instance)
        # return HttpResponse(json.dumps(dict_instance, cls=CJsonEncoder), content_type="application/json")

    @classmethod
    def text_response(cls, text: str):
        return HttpResponse(text, content_type="text/html")

    @classmethod
    def error_json_message(cls, message: str = None):
        return cls.json_response({"status": 1, "message": message})

    @classmethod
    def ok_json_message(cls, message: str = None):
        return cls.json_response({"status": 0, "message": message})

    @classmethod
    def ok_data(cls, data=None):
        obj = {"status": 0}
        if data:
            obj['data'] = data
        return cls.json_response(obj)

    @classmethod
    def ok_list_json(cls, obj_list, include_fields=[], exclude_fields=[]):
        fields = include_fields
        if obj_list and not fields:  # obj_list 必须为真    fields必须为假    obj_list and not fields 此表达式才为真
            fields = [f for f in get_model_fields_without_relation(obj_list[0].__class__) if f not in exclude_fields]
        return cls.json_response({"status": 0, "data": to_json(obj_list, fields)})

    @classmethod
    def ok_object_json(cls, obj, include_fields=[], exclude_fields=[]):
        if obj:
            fields = include_fields or []
            if not fields:
                fields = [f for f in get_model_fields_without_relation(obj.__class__) if f not in exclude_fields]

            return cls.json_response({"status": 0, "data": to_json(obj, fields)})
        else:
            return cls.json_response({"status": 1})

    def int_param(self, param_name, default=0) -> int:
        return int_param(self.request, param_name, default)

    def bool_param(self, param_name, default=False) -> bool:
        return bool_param(self.request, param_name, default)

    def param(self, key, default=None) -> str:
        return param(self.request, key, default)

    def mac(self):
        return (self.param("mac", "") or self.param("imei", "")).upper()

    def file_json_response(self, file):
        return self.json_response(load_json(file))


class ApiView(AcminView):
    _function_name = "api"


class WebView(AcminView):
    _function_name = "web"


def url(param=None):
    if isfunction(param):
        param.url = "/" + param.__name__
        return get_wrapper(param)
    else:
        def decorate(func):
            if param is None:
                path = func.__name__
            else:
                path = param[1:] if param and param.startswith("/") else param
            func.url = "/" + path
            return get_wrapper(func)

        return decorate


def load_json(file):
    base = settings.BASE_DIR
    with open(f"{base}/data/{file}", 'r', encoding="UTF-8") as load_f:
        return json.load(load_f)
