# Generated by Django 3.1.4 on 2021-05-31 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0002_auto_20210531_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_agent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_organisor',
            field=models.BooleanField(default=True),
        ),
    ]
