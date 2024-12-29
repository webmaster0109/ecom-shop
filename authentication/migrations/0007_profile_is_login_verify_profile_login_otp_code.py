# Generated by Django 5.1.4 on 2024-12-28 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_rename_updated_profile_modified_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_login_verify',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='login_otp_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]