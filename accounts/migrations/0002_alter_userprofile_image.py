# Generated by Django 4.1.1 on 2022-11-12 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default="{% static 'img/default.png' %}", upload_to='userprofile'),
        ),
    ]
