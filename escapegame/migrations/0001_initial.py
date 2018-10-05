# Generated by Django 2.0.7 on 2018-10-05 11:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('multimedia', '0001_initial'),
        ('controllers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EscapeGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('time_limit', models.DurationField(default=datetime.timedelta(0, 3600))),
                ('controller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='controllers.RaspberryPi')),
                ('map_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='game_map_image', to='multimedia.Image')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='EscapeGameChallenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('callback_url_solve', models.URLField(default='')),
                ('callback_url_reset', models.URLField(default='')),
                ('challenge_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='challenge_image', to='multimedia.Image')),
                ('challenge_solved_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='challenge_solved_image', to='multimedia.Image')),
                ('dependent_on', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='escapegame.EscapeGameChallenge')),
                ('gpio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='challenge_gpio', to='controllers.ChallengeGPIO')),
            ],
            options={
                'ordering': ['id', 'room', 'name'],
            },
        ),
        migrations.CreateModel(
            name='EscapeGameCube',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('tag_id', models.CharField(default='FFFFFFFF', max_length=8)),
                ('cube_delay', models.DurationField(default=datetime.timedelta(0, 30))),
                ('briefing_media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='escapegame_cube_briefing_media', to='multimedia.MultimediaFile')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='escapegame.EscapeGame')),
                ('losers_media', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='escapegamecube_losers_media', to='multimedia.MultimediaFile')),
                ('winners_media', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='escapegamecube_winners_media', to='multimedia.MultimediaFile')),
            ],
        ),
        migrations.CreateModel(
            name='EscapeGameRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('starts_the_timer', models.BooleanField(default=False)),
                ('stops_the_timer', models.BooleanField(default=False)),
                ('has_no_challenge', models.BooleanField(default=False)),
                ('controller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='controllers.RaspberryPi')),
                ('dependent_on', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='escapegame.EscapeGameRoom')),
                ('door', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room_door', to='controllers.DoorGPIO')),
                ('door_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='door_image', to='multimedia.Image')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='escapegame.EscapeGame')),
                ('room_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room_image', to='multimedia.Image')),
            ],
            options={
                'ordering': ['id', 'game', 'name'],
            },
        ),
        migrations.AddField(
            model_name='escapegamechallenge',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='escapegame.EscapeGameRoom'),
        ),
        migrations.AddField(
            model_name='escapegamechallenge',
            name='solved_media',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solved_media', to='multimedia.MultimediaFile'),
        ),
    ]
