# Generated by Django 3.2.7 on 2021-10-02 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0016_profile_current_money'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='current_money',
        ),
    ]