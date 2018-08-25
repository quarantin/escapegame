# Generated by Django 2.0.7 on 2018-08-22 23:50

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
                ('slug', models.SlugField(max_length=255)),
                ('escapegame_name', models.CharField(default='', max_length=255)),
                ('sas_door_pin', models.IntegerField(default=7)),
                ('corridor_door_pin', models.IntegerField(default=10)),
                ('sas_door_locked', models.BooleanField(default=True)),
                ('corridor_door_locked', models.BooleanField(default=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('corridor_door_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='corridor_door_image', to='multimedia.Image')),
                ('map_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='game_map_image', to='multimedia.Image')),
                ('raspberrypi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='escapegame_raspberrypi', to='controllers.RaspberryPi')),
                ('sas_door_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sas_door_image', to='multimedia.Image')),
                ('video', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='multimedia.Video')),
            ],
        ),
        migrations.CreateModel(
            name='EscapeGameChallenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255)),
                ('challenge_name', models.CharField(default='', max_length=255)),
                ('challenge_pin', models.IntegerField(default=31)),
                ('solved', models.BooleanField(default=False)),
                ('challenge_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='challenge_image', to='multimedia.Image')),
                ('challenge_solved_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='challenge_solved_image', to='multimedia.Image')),
            ],
        ),
        migrations.CreateModel(
            name='EscapeGameRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255)),
                ('room_name', models.CharField(default='', max_length=255)),
                ('door_pin', models.IntegerField(default=5)),
                ('door_locked', models.BooleanField(default=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('door_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='door_image', to='multimedia.Image')),
                ('escapegame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='escapegame.EscapeGame')),
                ('raspberrypi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='controllers.RaspberryPi')),
                ('room_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room_image', to='multimedia.Image')),
            ],
        ),
        migrations.AddField(
            model_name='escapegamechallenge',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='escapegame.EscapeGameRoom'),
        ),
    ]
