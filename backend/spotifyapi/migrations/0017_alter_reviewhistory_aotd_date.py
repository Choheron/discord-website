# Generated by Django 5.1.4 on 2025-01-10 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotifyapi', '0016_alter_review_aotd_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewhistory',
            name='aotd_date',
            field=models.DateField(),
        ),
    ]
