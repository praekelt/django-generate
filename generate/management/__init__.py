from django.conf import settings
from django.db.models import signals

def generate(app, created_models, verbosity, **kwargs):
    from django.core.management import call_command
    if kwargs.get('interactive', True):
        msg = "\nInstallation complete. Do you want to genererate default content? (yes/no): "
        confirm = raw_input(msg)
        while 1:
            if confirm not in ('yes', 'no'):
                confirm = raw_input('Please enter either "yes" or "no": ')
                continue
            if confirm == 'yes':
                call_command("generate", interactive=True)
            break

last_app = __import__("%s.models" % settings.INSTALLED_APPS[-1], globals(), locals(), ['models', ], -1)
signals.post_syncdb.connect(generate, sender=last_app)
