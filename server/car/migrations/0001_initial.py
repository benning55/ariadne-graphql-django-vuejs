# Generated by Django 3.0.2 on 2020-03-07 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('model', models.CharField(max_length=40)),
                ('price', models.IntegerField()),
            ],
        ),
    ]
