# Generated by Django 4.1.4 on 2023-01-20 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uploading', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fees_update',
            name='datebirth',
        ),
    ]
