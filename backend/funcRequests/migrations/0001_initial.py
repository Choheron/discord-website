# Generated by Django 5.1.4 on 2025-03-25 17:33

import django.db.models.deletion
import funcRequests.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0010_user_timezone_string'),
    ]

    operations = [
        migrations.CreateModel(
            name='FunctionalityRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('public_id', models.CharField(default=funcRequests.models.generate_public_id, editable=False, max_length=10, unique=True)),
                ('status', models.CharField(choices=[('pending', '🟡 Pending'), ('under_review', '🔍 Under Review'), ('approved', '✅ Approved'), ('in_progress', '🚧 In Progress'), ('implemented', '🚀 Implemented'), ('rejected', '❌ Rejected')], default='pending', max_length=20)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('reviewed_at', models.DateTimeField(blank=True, null=True)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('in_progress_at', models.DateTimeField(blank=True, null=True)),
                ('implemented_at', models.DateTimeField(blank=True, null=True)),
                ('rejected_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='FunctionalityRequestUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('changes', models.JSONField()),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updates', to='funcRequests.functionalityrequest')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.user')),
            ],
        ),
    ]
