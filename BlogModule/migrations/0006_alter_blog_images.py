# Generated by Django 5.2 on 2025-04-28 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogModule', '0005_remove_blog_image_blog_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='images',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
