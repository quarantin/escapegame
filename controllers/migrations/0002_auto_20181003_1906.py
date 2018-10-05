# Generated by Django 2.0.7 on 2018-10-03 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('escapegame', '0001_initial'),
        ('controllers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='liftgpio',
            name='cube',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='escapegame.EscapeGameCube'),
        ),
        migrations.AddField(
            model_name='gpio',
            name='controller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='controllers.Controller'),
        ),
        migrations.AddField(
            model_name='raspberrypi',
            name='game',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='escapegame.EscapeGame'),
        ),
        migrations.AddField(
            model_name='doorgpio',
            name='dependent_on',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='escapegame.EscapeGameChallenge'),
        ),
        migrations.AddField(
            model_name='challengegpio',
            name='cube',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='escapegame.EscapeGameCube'),
        ),
    ]