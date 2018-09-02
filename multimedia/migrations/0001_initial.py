# Generated by Django 2.0.7 on 2018-09-02 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(max_length=255, unique=True)),
                ('image_path', models.ImageField(upload_to='uploads/images')),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
            ],
            options={
                'ordering': ['image_name'],
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('video_name', models.CharField(max_length=255, unique=True)),
                ('video_path', models.FileField(upload_to='uploads/videos')),
            ],
            options={
                'ordering': ['video_name'],
            },
        ),
    ]
