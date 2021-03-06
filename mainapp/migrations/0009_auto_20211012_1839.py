# Generated by Django 3.2.7 on 2021-10-12 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_auto_20211012_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='cdekcities',
            name='cdek',
            field=models.BooleanField(default=False, verbose_name='Наличие пунктов СДЭК'),
        ),
        migrations.AddField(
            model_name='cdekcities',
            name='country',
            field=models.ForeignKey(blank=True, max_length=5, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.cdekcountry', verbose_name='Страна'),
        ),
        migrations.AddField(
            model_name='cdekcities',
            name='delivery_period_max',
            field=models.IntegerField(null=True, verbose_name='Максимальный срок доставки'),
        ),
        migrations.AddField(
            model_name='cdekcities',
            name='delivery_period_min',
            field=models.IntegerField(null=True, verbose_name='Минимальный срок доставки'),
        ),
        migrations.AddField(
            model_name='cdekcities',
            name='delivery_price',
            field=models.DecimalField(decimal_places=2, max_digits=9, null=True, verbose_name='Стоимость доставки'),
        ),
        migrations.AddField(
            model_name='cdekcities',
            name='latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Широта нас. пункта'),
        ),
        migrations.AddField(
            model_name='cdekcities',
            name='longitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Долгота нас. пункта'),
        ),
        migrations.AddField(
            model_name='cdekcities',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.cdekregions', verbose_name='Регион'),
        ),
        migrations.AddField(
            model_name='cdekcities',
            name='title',
            field=models.CharField(default='Город', max_length=255, verbose_name='Название'),
            preserve_default=False,
        ),
    ]
