# Generated by Django 3.0.5 on 2020-04-16 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendomatic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='beverage',
            name='stock',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
