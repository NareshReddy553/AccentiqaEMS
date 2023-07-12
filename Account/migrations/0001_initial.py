# Generated by Django 3.2.16 on 2023-07-12 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserPasswords',
            fields=[
                ('user_password_id', models.IntegerField(primary_key=True, serialize=False)),
                ('password', models.CharField(blank=True, max_length=200, null=True)),
                ('created_datetime', models.DateTimeField(blank=True, null=True)),
                ('modified_datetime', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'User_Passwords',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('user_name', models.CharField(max_length=100, unique=True)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('is_active', models.IntegerField()),
                ('created_datetime', models.DateTimeField(blank=True, null=True)),
                ('modified_datetime', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Users',
                'managed': False,
            },
        ),
    ]