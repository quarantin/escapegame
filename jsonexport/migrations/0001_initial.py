# Generated by Django 2.0.7 on 2018-09-10 14:13

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
            ],
            options={
                'verbose_name_plural': 'JSON Export',
                'verbose_name': 'JSON Export',
            },
        ),
        migrations.CreateModel(
            name='JsonImport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json_configuration', models.FileField(upload_to='')),
            ],
            options={
                'verbose_name_plural': 'JSON Import',
                'verbose_name': 'JSON Import',
            },
        ),
    ]
