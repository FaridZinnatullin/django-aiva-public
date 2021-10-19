# Generated by Django 3.2.7 on 2021-10-12 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_products', to='mainapp.series'),
        ),
    ]
