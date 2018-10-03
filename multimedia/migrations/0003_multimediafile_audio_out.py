# Generated by Django 2.0.7 on 2018-10-03 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia', '0002_multimediafile_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='multimediafile',
            name='audio_out',
            field=models.CharField(choices=[('hdmi', 'HDMI'), ('local', 'Headphone'), ('both', 'Both')], default='both', max_length=6),
        ),
    ]
