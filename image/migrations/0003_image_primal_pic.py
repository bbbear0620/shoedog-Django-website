# Generated by Django 2.0 on 2018-05-16 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0002_auto_20180507_0346'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='primal_pic',
            field=models.BooleanField(default=False),
        ),
    ]
