# Generated by Django 3.2.13 on 2022-06-27 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='price',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=10),
        ),
    ]
