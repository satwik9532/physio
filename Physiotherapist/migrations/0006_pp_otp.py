# Generated by Django 3.2.3 on 2021-06-01 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Physiotherapist', '0005_auto_20210526_1959'),
    ]

    operations = [
        migrations.CreateModel(
            name='pp_otp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('otp', models.IntegerField()),
                ('created_at', models.TimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'pp_otp',
            },
        ),
    ]
