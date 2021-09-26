# Generated by Django 3.2.7 on 2021-09-26 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0009_alter_expence_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budget',
            name='expence',
        ),
        migrations.RemoveField(
            model_name='expence',
            name='profile',
        ),
        migrations.AddField(
            model_name='expence',
            name='budget',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='viewer.budget'),
        ),
    ]