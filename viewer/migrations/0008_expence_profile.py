# Generated by Django 3.2.7 on 2021-09-26 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0007_delete_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='expence',
            name='profile',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='viewer.profile'),
        ),
    ]
