from django.apps import AppConfig


class AcminConfig(AppConfig):
    name = 'acmin'

    def ready(self):
        from acmin import sql
        from acmin import cache
        sql.patch()
        cache.patch()
