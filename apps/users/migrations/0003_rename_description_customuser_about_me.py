# Generated by Django 4.1.5 on 2023-01-19 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='description',
            new_name='about_me',
        ),
    ]
