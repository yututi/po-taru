# Generated by Django 2.2.3 on 2019-07-18 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RssInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=40)),
                ('url', models.URLField()),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=300)),
                ('link', models.URLField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('img', models.URLField()),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rss.RssInfo')),
            ],
        ),
    ]
