# Generated by Django 2.2.3 on 2019-07-18 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rss', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='rssinfo',
            name='last_updated',
            field=models.DateTimeField(),
        ),
    ]
