# Generated by Django 4.1.1 on 2022-11-09 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_delivered_items_image_delivered_items_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivered_items',
            name='image',
            field=models.ImageField(blank=True, upload_to='delivered_items'),
        ),
        migrations.AlterField(
            model_name='delivered_items',
            name='price',
            field=models.IntegerField(),
        ),
    ]
