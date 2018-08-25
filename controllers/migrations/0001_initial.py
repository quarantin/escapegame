# Generated by Django 2.0.7 on 2018-08-22 23:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RaspberryPi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('hostname', models.CharField(max_length=32)),
                ('port', models.IntegerField(default=80)),
            ],
            options={
                'verbose_name_plural': 'Raspberry Pis',
                'verbose_name': 'Raspberry Pi',
            },
        ),
        migrations.CreateModel(
            name='RemoteChallengePin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url_callback_validate', models.URLField(max_length=255)),
                ('url_callback_reset', models.URLField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='RemoteDoorPin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url_callback_lock', models.URLField(max_length=255)),
                ('url_callback_unlock', models.URLField(max_length=255)),
                ('raspberrypi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='controllers.RaspberryPi')),
            ],
        ),
        migrations.CreateModel(
            name='RemoteLedPin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('pin_number', models.IntegerField(default=7)),
                ('url_on', models.URLField(max_length=255)),
                ('url_off', models.URLField(max_length=255)),
                ('raspberrypi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='controllers.RaspberryPi')),
            ],
            options={
                'verbose_name_plural': 'Remote LED pins',
                'verbose_name': 'Remote LED pin',
            },
        ),
    ]
