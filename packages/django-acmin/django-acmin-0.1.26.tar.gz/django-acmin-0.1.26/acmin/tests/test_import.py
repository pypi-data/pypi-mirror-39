from django.test import TestCase

from acmin.utils import import_class


class Case(TestCase):
    def test_import_class(self):
        from acmin.forms import load_form
        #print(load_form("admin","BB"))
