# Generated by Django 5.0.3 on 2024-04-10 17:38

import myapp.models.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_userprofile_user_imag_container_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user_permissions',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_imag_container',
            field=models.ImageField(blank=True, null=True, upload_to='', validators=[myapp.models.models.validate_image_file_size]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_profile_imag',
            field=models.ImageField(blank=True, default=myapp.models.models.default_image, null=True, upload_to=''),
        ),
    ]
