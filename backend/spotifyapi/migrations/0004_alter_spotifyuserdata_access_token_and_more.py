# Generated by Django 5.0.6 on 2024-11-16 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotifyapi', '0003_spotifyuserdata_access_token_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spotifyuserdata',
            name='access_token',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='spotifyuserdata',
            name='refresh_token',
            field=models.CharField(max_length=512, null=True),
        ),
    ]
