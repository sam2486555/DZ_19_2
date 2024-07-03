# Generated by Django 5.0.6 on 2024-07-03 09:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='product',
            field=models.ForeignKey(blank='True', null='True', on_delete=django.db.models.deletion.CASCADE, related_name='Версия', to='catalog.product', verbose_name='Продукт'),
        ),
    ]
