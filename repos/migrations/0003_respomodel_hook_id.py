# Generated by Django 3.0.7 on 2020-06-13 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repos', '0002_webhookeventmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='respomodel',
            name='hook_id',
            field=models.CharField(default=1, max_length=40),
            preserve_default=False,
        ),
    ]