# Generated by Django 2.0.7 on 2018-09-24 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('controllers', '0001_initial'),
        ('multimedia', '0001_initial'),
        ('escapegame', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='liftgpio',
            name='game',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='escapegame.EscapeGame'),
        ),
        migrations.AddField(
            model_name='liftgpio',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='multimedia.Image'),
        ),
        migrations.AddField(
            model_name='liftgpio',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='multimedia.Video'),
        ),
        migrations.AddField(
            model_name='gpio',
            name='controller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='controllers.Controller'),
        ),
        migrations.AddField(
            model_name='gpio',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='multimedia.Image'),
        ),
        migrations.AddField(
            model_name='doorgpio',
            name='game',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='escapegame.EscapeGame'),
        ),
        migrations.AddField(
            model_name='doorgpio',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='escapegame.EscapeGameRoom'),
        ),
        migrations.AddField(
            model_name='challengegpio',
            name='cube',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='escapegame.EscapeGameCube'),
        ),
    ]
