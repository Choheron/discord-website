# Generated by Django 5.1.4 on 2025-04-12 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotifyapi', '0029_alter_dailyalbum_rating_timeline'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyalbum',
            name='rating',
            field=models.FloatField(default=11.0),
        ),
    ]
