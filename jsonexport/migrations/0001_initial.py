# Generated by Django 2.0.7 on 2018-08-30 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JsonExport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indent', models.BooleanField(default=True)),
                ('export_date', models.BooleanField(default=True)),
                ('software_version', models.BooleanField(default=True)),
                ('images', models.BooleanField(default=True)),
                ('videos', models.BooleanField(default=True)),
                ('video_players', models.BooleanField(default=True)),
                ('escapegames', models.BooleanField(default=True)),
                ('rooms', models.BooleanField(default=True)),
                ('challenges', models.BooleanField(default=True)),
                ('raspberry_pis', models.BooleanField(default=True)),
                ('remote_challenge_pins', models.BooleanField(default=True)),
                ('remote_door_pins', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'JSON Export',
                'verbose_name_plural': 'JSON Export',
            },
        ),
        migrations.CreateModel(
            name='JsonImport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json_configuration', models.FileField(upload_to='')),
            ],
            options={
                'verbose_name': 'JSON Import',
                'verbose_name_plural': 'JSON Import',
            },
        ),
    ]
