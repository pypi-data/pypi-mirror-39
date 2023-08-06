def init_models(sender, **kwargs):
    from acmin.models.field import init_fields
    from acmin.models.contenttype import init_contenttype
    type_map = init_contenttype()
    init_fields(type_map)
