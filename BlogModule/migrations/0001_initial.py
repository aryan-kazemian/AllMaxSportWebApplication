# Generated by Django 5.2 on 2025-04-19 20:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('excerpt', models.TextField(blank=True, null=True)),
                ('meta_description', models.TextField(blank=True, null=True)),
                ('keywords', models.CharField(blank=True, max_length=500)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10)),
                ('featured_image', models.ImageField(blank=True, null=True, upload_to='blog/featured_images/')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modify_date', models.DateTimeField(auto_now=True)),
                ('seo_score', models.PositiveIntegerField(default=0)),
                ('seo_score_color', models.CharField(default='text-gray-500', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SEOStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_length_status', models.CharField(choices=[('ok', 'OK'), ('warning', 'Warning'), ('error', 'Error')], max_length=10)),
                ('title_length_message', models.TextField()),
                ('content_length_status', models.CharField(choices=[('ok', 'OK'), ('warning', 'Warning'), ('error', 'Error')], max_length=10)),
                ('content_length_message', models.TextField()),
                ('keyword_density_status', models.CharField(choices=[('ok', 'OK'), ('warning', 'Warning'), ('error', 'Error')], max_length=10)),
                ('keyword_density_message', models.TextField()),
                ('meta_description_status', models.CharField(choices=[('ok', 'OK'), ('warning', 'Warning'), ('error', 'Error')], max_length=10)),
                ('meta_description_message', models.TextField()),
                ('headings_status', models.CharField(choices=[('ok', 'OK'), ('warning', 'Warning'), ('error', 'Error')], max_length=10)),
                ('headings_message', models.TextField()),
                ('images_status', models.CharField(choices=[('ok', 'OK'), ('warning', 'Warning'), ('error', 'Error')], max_length=10)),
                ('images_message', models.TextField()),
                ('internal_links_status', models.CharField(choices=[('ok', 'OK'), ('warning', 'Warning'), ('error', 'Error')], max_length=10)),
                ('internal_links_message', models.TextField()),
                ('blog', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='seo_status', to='BlogModule.blog')),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=models.ManyToManyField(blank=True, to='BlogModule.tag'),
        ),
    ]
