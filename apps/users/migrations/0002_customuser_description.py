# Generated by Django 4.1.5 on 2023-01-19 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='description',
            field=models.CharField(blank=True, max_length=128, verbose_name='о себе'),
        ),
    ]