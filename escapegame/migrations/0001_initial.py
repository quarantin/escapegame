# Generated by Django 2.0.7 on 2018-08-05 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Arduino',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('slug', models.SlugField(editable=False, max_length=255)),
                ('ip_address', models.CharField(max_length=16)),
                ('code_template', models.FileField(upload_to='uploads')),
            ],
        ),
        migrations.CreateModel(
            name='EscapeGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('escape_game_name', models.CharField(default='', max_length=255)),
                ('slug', models.SlugField(editable=False, max_length=255)),
                ('sas_door_pin', models.IntegerField(default=7)),
                ('corridor_door_pin', models.IntegerField(default=9)),
                ('sas_door_locked', models.BooleanField(default=True)),
                ('corridor_door_locked', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='EscapeGameChallenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('challenge_name', models.CharField(default='', max_length=255)),
                ('slug', models.SlugField(editable=False, max_length=255)),
                ('solved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='EscapeGameRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(default='', max_length=255)),
                ('slug', models.SlugField(editable=False, max_length=255)),
                ('door_pin', models.IntegerField(default=5)),
                ('door_locked', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_type', models.CharField(choices=[('challenge', 'Challenge'), ('door', 'Door'), ('map', 'Map'), ('room', 'Room')], default='room', max_length=255)),
                ('image_path', models.ImageField(upload_to='uploads')),
            ],
        ),
        migrations.CreateModel(
            name='RaspberryPi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('hostname', models.CharField(max_length=32)),
                ('port', models.IntegerField(default=8000)),
            ],
        ),
        migrations.CreateModel(
            name='RemotePin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('pin_type', models.CharField(choices=[('led', 'Led'), ('door', 'Door'), ('challenge', 'Challenge')], max_length=16)),
                ('pin_number', models.IntegerField(default=7)),
                ('callback_url', models.URLField(max_length=255)),
                ('raspberrypi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='escapegame.RaspberryPi')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_name', models.CharField(max_length=255)),
                ('video_path', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='VideoPlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_player', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='escapegameroom',
            name='door_image_path',
            field=models.ForeignKey(blank=True, limit_choices_to={'image_type': 'door'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room_door_image_path', to='escapegame.Image'),
        ),
        migrations.AddField(
            model_name='escapegameroom',
            name='escape_game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='escapegame.EscapeGame'),
        ),
        migrations.AddField(
            model_name='escapegameroom',
            name='room_controller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='escapegame.RaspberryPi'),
        ),
        migrations.AddField(
            model_name='escapegameroom',
            name='room_image_path',
            field=models.ForeignKey(blank=True, limit_choices_to={'image_type': 'room'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room_image_path', to='escapegame.Image'),
        ),
        migrations.AddField(
            model_name='escapegamechallenge',
            name='challenge_image_path',
            field=models.ForeignKey(blank=True, limit_choices_to={'image_type': 'challenge'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chall_map_image_path', to='escapegame.Image'),
        ),
        migrations.AddField(
            model_name='escapegamechallenge',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='escapegame.EscapeGameRoom'),
        ),
        migrations.AddField(
            model_name='escapegame',
            name='corridor_door_image_path',
            field=models.ForeignKey(blank=True, limit_choices_to={'image_type': 'door'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='corridor_door_image_path', to='escapegame.Image'),
        ),
        migrations.AddField(
            model_name='escapegame',
            name='escape_game_controller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='escapegame.RaspberryPi'),
        ),
        migrations.AddField(
            model_name='escapegame',
            name='map_image_path',
            field=models.ForeignKey(blank=True, limit_choices_to={'image_type': 'map'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_map_image_path', to='escapegame.Image'),
        ),
        migrations.AddField(
            model_name='escapegame',
            name='sas_door_image_path',
            field=models.ForeignKey(blank=True, limit_choices_to={'image_type': 'door'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sas_door_image_path', to='escapegame.Image'),
        ),
        migrations.AddField(
            model_name='escapegame',
            name='video_brief',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='escapegame.Video'),
        ),
    ]
