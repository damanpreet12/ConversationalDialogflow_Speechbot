# Generated by Django 3.1.3 on 2020-11-08 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speechbot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='age',
            field=models.IntegerField(default=''),
        ),
    ]
