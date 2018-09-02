# Generated by Django 2.0.7 on 2018-09-02 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArduinoSketch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sketch_name', models.CharField(max_length=255, unique=True)),
                ('sketch_code', models.TextField(max_length=10000)),
                ('sketch_path', models.FileField(upload_to='uploads/sketches')),
            ],
            options={
                'verbose_name': 'Arduino Sketch',
                'verbose_name_plural': 'Arduino Sketches',
            },
        ),
        migrations.CreateModel(
            name='RaspberryPi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('hostname', models.CharField(max_length=255, unique=True)),
                ('port', models.IntegerField(default=80)),
            ],
            options={
                'verbose_name': 'Raspberry Pi',
                'verbose_name_plural': 'Raspberry Pis',
            },
        ),
    ]
