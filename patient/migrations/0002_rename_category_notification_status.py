# Generated by Django 5.1.4 on 2025-02-18 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='category',
            new_name='status',
        ),
    ]
