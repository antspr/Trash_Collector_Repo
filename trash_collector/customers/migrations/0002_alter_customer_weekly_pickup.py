# Generated by Django 3.2.9 on 2021-11-05 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='weekly_pickup',
            field=models.CharField(max_length=10),
        ),
    ]