# Generated by Django 5.0.6 on 2024-06-08 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_activateaccount_email_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='followee',
            new_name='followerss',
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('followerss', 'follower_user'), name='unique_follow'),
        ),
    ]
