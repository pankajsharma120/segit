# Generated by Django 3.0.7 on 2020-06-12 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200612_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='githubaccountmodel',
            name='git_username',
            field=models.CharField(default=1, max_length=120),
            preserve_default=False,
        ),
    ]
