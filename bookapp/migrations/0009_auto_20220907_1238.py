# Generated by Django 3.2.6 on 2022-09-07 11:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookapp', '0008_review_review_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='rating',
        ),
        migrations.AddField(
            model_name='book',
            name='average_rating',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AddField(
            model_name='book',
            name='no_reviews',
            field=models.PositiveIntegerField(default=0),
        ),
    ]