# Generated by Django 3.2.6 on 2021-08-30 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='input',
        ),
        migrations.RemoveField(
            model_name='problem',
            name='output',
        ),
    ]
