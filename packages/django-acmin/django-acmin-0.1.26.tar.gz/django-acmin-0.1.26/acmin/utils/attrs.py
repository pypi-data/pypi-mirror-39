import datetime


def attr2(obj, name, default, show_display=False):
    result = None
    if isinstance(obj, dict):
        result = obj.get(name, default)
    elif isinstance(obj, (list, tuple)):
        try:
            result = obj[int(name)]
        except Exception:
            result = None
    elif hasattr(obj, name):
        if show_display:
            dispaly_method = 'get_' + name + '_display'
            if hasattr(obj, dispaly_method):
                method = getattr(obj, dispaly_method)
                result = method()
            else:
                result = getattr(obj, name)
        else:
            result = getattr(obj, name)

    return result


def attr(obj, attr_name, default=None, show_display=False):
    name = str(attr_name).strip()
    result = None
    if obj is not None:
        if "." not in name:
            result = attr2(obj, name, default, show_display)
        else:
            parts = name.split(".", 1)
            result = attr(attr(obj, parts[0]), parts[1])

    if result is None:
        result = default
    return result


get = attr


def set(obj, name, value):
    setattr(obj, name, value)
    return obj


def display(obj, attr_name):
    result = attr(obj, attr_name, default="", show_display=True)
    if isinstance(result, bool):
        result = "是" if result else '否'
    elif isinstance(result, datetime.datetime):
        result = result.strftime("%Y-%m-%d %H:%M:%S")
    return result
