# Generated by Django 4.1.1 on 2022-11-11 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_blog_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='image1',
            new_name='image',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='image2',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='image3',
        ),
    ]
