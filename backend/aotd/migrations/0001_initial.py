# Generated by Django 5.1.4 on 2025-05-29 20:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0011_alter_user_options_alter_user_managers_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AotdUserData',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='aotd_data', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True)),
                ('selection_blocked_flag', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mbid', models.CharField(max_length=256, unique=True)),
                ('title', models.CharField(max_length=256)),
                ('artist', models.CharField(max_length=256)),
                ('artist_url', models.CharField(default='', max_length=512)),
                ('cover_url', models.CharField(max_length=512)),
                ('album_url', models.CharField(default='', max_length=512)),
                ('user_comment', models.TextField(blank=True, null=True)),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('release_date', models.DateField(max_length=50, null=True)),
                ('release_date_str', models.CharField(max_length=50, null=True)),
                ('raw_data', models.JSONField(null=True)),
                ('track_list', models.JSONField(null=True)),
                ('submitted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='submitted_albums', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
