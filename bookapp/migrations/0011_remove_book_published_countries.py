# Generated by Django 3.2.6 on 2022-09-21 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookapp', '0010_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='published_countries',
        ),
    ]
