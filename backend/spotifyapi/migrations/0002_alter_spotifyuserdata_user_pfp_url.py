# Generated by Django 5.0.6 on 2024-11-13 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotifyapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spotifyuserdata',
            name='user_pfp_url',
            field=models.CharField(max_length=512, null=True),
        ),
    ]