# Generated by Django 5.1.4 on 2025-02-19 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0002_user_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_role',
            field=models.CharField(blank=True, choices=[('Doctor', 'Doctor'), ('Patient', 'Patient')], max_length=20, null=True),
        ),
    ]
