# Generated by Django 3.1.6 on 2021-10-29 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20211029_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='contentType',
            field=models.CharField(choices=[('plain', 'text/plain'), ('markdown', 'text/markdown'), ('jpeg', 'image/jpeg;base64'), ('app', 'application/base64'), ('png', 'image/png;base64')], default='plain', max_length=20),
        ),
    ]
