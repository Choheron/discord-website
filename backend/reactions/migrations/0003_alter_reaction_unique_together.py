# Generated by Django 5.1.4 on 2025-04-08 22:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reactions', '0002_rename_created_at_reaction_creation_timestamp_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reaction',
            unique_together=set(),
        ),
    ]
