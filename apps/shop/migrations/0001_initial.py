# Generated by Django 4.1.5 on 2023-01-17 23:05

import apps.shop.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='название бренда')),
            ],
            options={
                'verbose_name': 'бренд',
                'verbose_name_plural': 'бренды',
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=32, verbose_name='категория')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='название')),
                ('description', models.TextField(max_length=1024, verbose_name='описание')),
                ('image', models.ImageField(upload_to=apps.shop.models.image_folder)),
                ('price', models.PositiveIntegerField(editable=False, help_text='цена товара со скидкой', verbose_name='цена со скидкой')),
                ('real_price', models.PositiveIntegerField(help_text='цена товара', verbose_name='реальная цена')),
                ('discount', models.PositiveSmallIntegerField(default=0, validators=[apps.shop.models.validate_discount], verbose_name='скидка (%)')),
                ('rating', models.DecimalField(decimal_places=1, default=apps.shop.models.get_random_rating, max_digits=2, verbose_name='рейтинг (1-5)')),
                ('amount', models.PositiveSmallIntegerField(default=0, verbose_name='в наличии шт.')),
                ('count_sales', models.PositiveIntegerField(default=0, verbose_name='продано')),
                ('added_at', models.DateField(default=django.utils.timezone.now, verbose_name='поступило')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.brand', verbose_name='бренд')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.productcategory', verbose_name='категория')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
            },
        ),
    ]