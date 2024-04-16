# Generated by Django 5.0.3 on 2024-03-29 13:19

import django.core.validators
import myapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_imag_container',
            field=models.ImageField(blank=True, null=True, upload_to='User_pics/uploaded_pics', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'heic']), myapp.models.validate_image_file_size]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_profile_imag',
            field=models.ImageField(blank=True, null=True, upload_to='User_pics/profile_pics', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'heic']), myapp.models.validate_image_file_size]),
        ),
    ]
