# Generated by Django 5.1.1 on 2024-11-20 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0009_remove_savedrecipe_saved_at_nutritionalplan_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipienutritionalplan',
            name='meal_type',
            field=models.CharField(choices=[('ESMORZAR', 'Breakfast'), ('DINAR', 'Lunch'), ('BERENAR', 'Snack'), ('SOPAR', 'Dinner')], max_length=20),
        ),
    ]
