# Generated by Django 5.1.4 on 2025-01-10 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotifyapi', '0014_review_aotd_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewhistory',
            name='aotd_date',
            field=models.DateField(default=None, null=True),
        ),
    ]
