# Generated by Django 3.2.8 on 2021-11-25 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0017_auto_20211123_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='contentType',
            field=models.CharField(choices=[('png', 'image/png;base64'), ('plain', 'text/plain'), ('markdown', 'text/markdown'), ('app', 'application/base64'), ('jpeg', 'image/jpeg;base64')], default='plain', max_length=20),
        ),
    ]
