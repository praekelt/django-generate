import cStringIO
import hashlib
import json
import mimetypes
import os
import random
import sys
import urllib
from datetime import datetime

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import get_model, DateField, DateTimeField, FileField, \
        ImageField
from django.db.models.fields.related import ManyToManyField
from django.db import transaction

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
USE_CACHE = True


def load_file(field, source):
    source = fetch_from_cache(source)
    size = os.path.getsize(source)
    f = cStringIO.StringIO()
    f.write(open(source, 'r').read())
    field_name = str(field)
    file_name = source.split('/')[-1]
    content_type = mimetypes.guess_type(file_name)[0]
    elements = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456890'
    file_name = '%s.%s' % (''.join([random.choice(elements) \
            for n in range(8)]), file_name.split('.')[-1])
    return InMemoryUploadedFile(f, field_name, file_name, content_type, size, \
            None)


def fetch_from_cache(source):
    destination = source
    if source.startswith('http'):
        destination = '%s/json_loader_cache/%s' % (SCRIPT_PATH, hashlib.\
                md5(source).hexdigest())
        if not USE_CACHE or not os.path.exists(destination):
            #print "Fetching %s..." % source
            f = open(destination, 'w')
            f.write(urllib.urlopen(source).read())
            f.close()
    return destination


@transaction.autocommit
def generate_item(item):
    app, model = item['model'].split('.')
    model = get_model(app, model)
    model_instance = model(pk='dummy_pk')
    fields = {}
    direct_foreign_key_fields = {}
    many_to_many_fields = {}
    image_fields = {}
    file_fields = {}
    password_field = ''

    if 'fields' in item:
        for field, value in item['fields'].items():

            # No need to recurse or process further if foreign key is provided
            if field.endswith('_id'):
                direct_foreign_key_fields[field] = value
                continue

            if value.__class__ == list:
                value_items = []
                for item in value:
                    if item.__class__ == dict:
                        value_items.append(generate_item(item))
                    else:
                        value_items.append(item)
                value = value_items
            elif value.__class__ == dict:
                value = generate_item(value)

            model_field = model_instance._meta.get_field(field)
            if isinstance(model_field, ManyToManyField):
                many_to_many_fields[str(field)] = value
            elif isinstance(model_field, ImageField):
                if value:
                    image_fields[str(field)] = value
            elif isinstance(model_field, FileField):
                if value:
                    file_fields[str(field)] = value
            elif field == 'password':
                password_field = value
            elif isinstance(model_field, DateTimeField):
                try:
                    fields[str(field)] = datetime.strptime(value, \
                            "%Y-%m-%d %H:%M:%S.%f")
                except ValueError:
                    fields[str(field)] = datetime.strptime(value, \
                            "%Y-%m-%d %H:%M:%S")
            elif isinstance(model_field, DateField):
                try:
                    fields[str(field)] = datetime.strptime(value, "%Y-%m-%d").\
                            date()
                except ValueError:
                    fields[str(field)] = datetime.strptime(value, \
                            "%Y-%m-%d %H:%M:%S")
            else:
                fields[str(field)] = value

    dirty = False
    if fields:
        obj, created = model.objects.get_or_create(**fields)

        if created and direct_foreign_key_fields:
            for k, v in direct_foreign_key_fields.items():
                current = getattr(obj, k)
                if current != v:
                    setattr(obj, k, v)
                    dirty = True

    else:
        existing = model.objects.all()
        if existing.exists():
            obj = existing[0]
            created = False
        else:
            obj = model()
            obj.save()
            created = True

    if created:
        #print "Created %s" % obj

        for field, value in many_to_many_fields.items():
            obj_field = getattr(obj, field)
            if value.__class__ == list:
                for val in value:
                    obj_field.add(val)
            else:
                obj_field.add(value)
            dirty = True

        for field, value in image_fields.items():
            field_attr = getattr(obj, field)
            f = load_file(field, value)
            field_attr.save(f.name, f)

        for field, value in file_fields.items():
            field_attr = getattr(obj, field)
            f = load_file(field, value)
            field_attr.save(f.name, f)
            dirty = True

        if password_field:
            obj.set_password(password_field)
            dirty = True

        if dirty:
            obj.save()

    return obj


def load_json(source, data_formatter=None):
    json_data = []
    if source.__class__ == str:
        source = fetch_from_cache(source)
        source = open(source, 'r')
        data = source.read()
        json_data = json.loads(data)
        source.close()
    elif source.__class__ == list:
        source = [str(item).replace("False", "false").replace("True", "true").\
                replace("'", '"') for item in source]
        json_data = json.loads("[%s]" % ','.join(source))

    if data_formatter:
        json_data = data_formatter(json_data)

    i = 1
    previous_status = ""
    for item in json_data:
        generate_item(item)
        status = "Generating items, please wait... %s%%" % (100 * i / len(\
                json_data))
        if status != previous_status:
            sys.stdout.write("\b" * len(status))
            sys.stdout.write(status)
            sys.stdout.flush()
        i += 1
    print ""
