from django.conf import settings
from django.db.models import signals


def generate(app, created_models, verbosity, **kwargs):
    from django.core.management import call_command
    if kwargs.get('interactive', True):
        msg = "\nInstallation complete. Do you want to genererate default \
                content? (yes/no): "
        confirm = raw_input(msg)
        while 1:
            if confirm not in ('yes', 'no'):
                confirm = raw_input('Please enter either "yes" or "no": ')
                continue
            if confirm == 'yes':
                call_command("generate", interactive=True)
            break

# Get last app with models.
last_app_with_models = None
for app in settings.INSTALLED_APPS:
    try:
        last_app_with_models = __import__("%s.models" % app, globals(), \
                locals(), ['models', ], -1)
    except ImportError:
        pass

# If we have a last app with models connect the
# post sync signal to generate content.
if last_app_with_models:
    signals.post_syncdb.connect(generate, sender=last_app_with_models)
