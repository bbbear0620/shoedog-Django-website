# Generated by Django 2.0 on 2018-04-20 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_statistic', '0002_readdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='readdetail',
            name='read_num',
            field=models.IntegerField(default=0),
        ),
    ]