# Generated by Django 2.0 on 2018-04-26 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commment',
            options={'ordering': ['-comment_time']},
        ),
    ]