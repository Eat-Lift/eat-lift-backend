# Generated by Django 5.1.1 on 2024-11-19 20:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0008_alter_recipe_picture'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='savedrecipe',
            name='saved_at',
        ),
        migrations.CreateModel(
            name='NutritionalPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nutritional_plan', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RecipieNutritionalPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_type', models.CharField(choices=[('Esmorzar', 'Breakfast'), ('DINAR', 'Lunch'), ('BERENAR', 'Snack'), ('SOPAR', 'Dinner')], max_length=20)),
                ('nutritional_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nutritional_plan_recipes', to='nutrition.nutritionalplan')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meal_recipes', to='nutrition.recipe')),
            ],
            options={
                'unique_together': {('nutritional_plan', 'meal_type', 'recipe')},
            },
        ),
    ]
