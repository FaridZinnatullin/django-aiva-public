# Generated by Django 3.2.7 on 2021-10-12 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20211012_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=555, max_digits=9, verbose_name='Цена'),
            preserve_default=False,
        ),
    ]
