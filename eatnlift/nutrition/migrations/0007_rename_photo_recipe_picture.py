# Generated by Django 5.1.1 on 2024-11-18 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0006_rename_grams_recipefooditem_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='photo',
            new_name='picture',
        ),
    ]