# Generated by Django 4.1.7 on 2023-04-28 11:23

from django.db import migrations
import uuid

def gen_uuid(apps, schema_editor):
    MyModel = apps.get_model('onlineStoreApp', 'Cart')
    for row in MyModel.objects.all():
        row.cart_key = uuid.uuid4()
        row.save(update_fields=['cart_key'])


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStoreApp', '0027_cart_cart_key_alter_cart_date'),
    ]

    operations = [
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]
