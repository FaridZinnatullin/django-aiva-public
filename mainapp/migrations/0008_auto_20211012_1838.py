# Generated by Django 3.2.7 on 2021-10-12 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_auto_20211012_1836'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cdekcities',
            name='cdek',
        ),
        migrations.RemoveField(
            model_name='cdekcities',
            name='country',
        ),
        migrations.RemoveField(
            model_name='cdekcities',
            name='delivery_period_max',
        ),
        migrations.RemoveField(
            model_name='cdekcities',
            name='delivery_period_min',
        ),
        migrations.RemoveField(
            model_name='cdekcities',
            name='delivery_price',
        ),
        migrations.RemoveField(
            model_name='cdekcities',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='cdekcities',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='cdekcities',
            name='region',
        ),
        migrations.RemoveField(
            model_name='cdekcities',
            name='title',
        ),
    ]