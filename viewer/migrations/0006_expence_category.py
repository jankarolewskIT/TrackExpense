# Generated by Django 3.2.7 on 2021-09-26 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0005_remove_expence_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='expence',
            name='category',
            field=models.CharField(choices=[('TR', 'Transport'), ('ET', 'Entertainment'), ('PH', 'Health'), ('CT', 'Clothes'), ('FD', 'Food'), ('AD', 'Accommodation'), ('OT', 'Others')], default='OT', max_length=2),
        ),
    ]
