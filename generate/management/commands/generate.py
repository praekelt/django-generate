import imp
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def handle(self, *app_labels, **options):
        from django.db.models import get_app, get_apps, get_models

        exclude = options.get('exclude', [])

        excluded_apps = [get_app(app_label) for app_label in exclude]

        if len(app_labels) == 0:
            app_list = [app for app in get_apps() if app not in excluded_apps]
        else:
            app_list = [get_app(app_label) for app_label in app_labels]

        for app in app_list:
            name = app.__name__.replace('.models', '')
            app_path = __import__(name, {}, {}, [name.split('.')[-1]]).__path__
            try:
                params = imp.find_module('generate', app_path)
            except ImportError:
                pass
            else:
                generate = imp.load_module(name + '.generate', *params)

                generate.generate()
