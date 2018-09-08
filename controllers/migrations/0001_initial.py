# Generated by Django 2.0.7 on 2018-09-08 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('multimedia', '0001_initial'),
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
                'verbose_name_plural': 'Arduino Sketches',
                'verbose_name': 'Arduino Sketch',
            },
        ),
        migrations.CreateModel(
            name='GPIO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('pin', models.IntegerField(default=7)),
            ],
            options={
                'verbose_name_plural': 'GPIOs',
                'verbose_name': 'GPIO',
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
                'verbose_name_plural': 'Raspberry Pis',
                'verbose_name': 'Raspberry Pi',
            },
        ),
        migrations.CreateModel(
            name='ChallengeGPIO',
            fields=[
                ('gpio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='controllers.GPIO')),
                ('solved', models.BooleanField(default=False)),
                ('solved_at', models.DateTimeField(blank=True, null=True)),
            ],
            bases=('controllers.gpio',),
        ),
        migrations.CreateModel(
            name='CubeGPIO',
            fields=[
                ('gpio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='controllers.GPIO')),
                ('tag_id', models.CharField(max_length=32)),
                ('taken_at', models.DateTimeField(blank=True, null=True)),
                ('placed_at', models.DateTimeField(blank=True, null=True)),
            ],
            bases=('controllers.gpio',),
        ),
        migrations.CreateModel(
            name='DoorGPIO',
            fields=[
                ('gpio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='controllers.GPIO')),
                ('locked', models.BooleanField(default=True)),
                ('unlocked_at', models.DateTimeField(blank=True, null=True)),
            ],
            bases=('controllers.gpio',),
        ),
        migrations.AddField(
            model_name='gpio',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='multimedia.Image'),
        ),
        migrations.AddField(
            model_name='gpio',
            name='raspberrypi',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='controllers.RaspberryPi'),
        ),
    ]
