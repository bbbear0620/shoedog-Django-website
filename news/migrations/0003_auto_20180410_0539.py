# Generated by Django 2.0 on 2018-04-10 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_anews_main_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anews',
            name='main_image',
            field=models.ImageField(default=None, upload_to='news_image/%Y/%m/%d'),
        ),
    ]
