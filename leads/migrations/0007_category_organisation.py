# Generated by Django 3.1.4 on 2021-05-31 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0006_auto_20210531_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='organisation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='leads.userprofile'),
        ),
    ]
