# Generated by Django 5.1.4 on 2025-02-11 23:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_last_request_timestamp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='last_request_timestamp',
            new_name='last_response_timestamp',
        ),
    ]
