# Generated by Django 5.1.4 on 2025-02-15 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotifyapi', '0019_review_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewhistory',
            name='version',
            field=models.IntegerField(default=1),
        ),
    ]
