# Generated by Django 2.0.7 on 2018-10-03 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('escapegame', '0001_initial'),
        ('multimedia', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='multimediafile',
            name='game',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='escapegame.EscapeGame'),
        ),
    ]