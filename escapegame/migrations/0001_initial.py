# Generated by Django 2.0.7 on 2018-10-02 14:09

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('controllers', '0001_initial'),
        ('multimedia', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EscapeGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('time_limit', models.DurationField(default=datetime.timedelta(0, 3600))),
                ('cube_delay', models.DurationField(default=datetime.timedelta(0, 30))),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('finish_time', models.DateTimeField(blank=True, null=True)),
                ('controller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='controllers.RaspberryPi')),
                ('losers_video', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='escapegame_losers_video', to='multimedia.Video')),
                ('map_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='game_map_image', to='multimedia.Image')),
                ('winners_video', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='escapegame_winners_video', to='multimedia.Video')),
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
                ('gpio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='challenge_gpio', to='controllers.ChallengeGPIO')),
            ],
            options={
                'ordering': ['id', 'room', 'name'],
            },
        ),
        migrations.CreateModel(
            name='EscapeGameCube',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_id', models.CharField(default='FFFFFFFF', max_length=8)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='escapegame.EscapeGame')),
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
                ('controller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='controllers.RaspberryPi')),
                ('door', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room_door', to='controllers.DoorGPIO')),
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
            name='solved_video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solved_video', to='multimedia.Video'),
        ),
    ]
