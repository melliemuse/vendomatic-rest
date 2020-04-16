# Generated by Django 3.0.5 on 2020-04-16 02:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Beverage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beverageType', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coinType', models.CharField(max_length=25)),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('coinId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendomatic.Coin')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('coinId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendomatic.Coin')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beverageId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendomatic.Beverage')),
                ('customerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendomatic.Customer')),
                ('paymentId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendomatic.Payment')),
            ],
        ),
    ]