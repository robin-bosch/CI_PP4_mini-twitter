# Generated by Django 4.1.4 on 2022-12-25 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_rename_status_postvote_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_picture',
            field=models.URLField(blank=True),
        ),
    ]
