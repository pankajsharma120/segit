# Generated by Django 3.0.7 on 2020-06-14 08:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repos', '0002_auto_20200614_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webhookeventmodel',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
