# Generated by Django 4.1.4 on 2022-12-25 01:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_user_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='followrelation',
            old_name='user_followed',
            new_name='followed_user',
        ),
    ]
