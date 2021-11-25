# Generated by Django 3.2.8 on 2021-11-25 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0025_alter_post_contenttype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='contentType',
            field=models.CharField(choices=[('plain', 'text/plain'), ('png', 'image/png;base64'), ('jpeg', 'image/jpeg;base64'), ('markdown', 'text/markdown'), ('app', 'application/base64')], default='plain', max_length=20),
        ),
        migrations.AlterField(
            model_name='post',
            name='visibility',
            field=models.CharField(choices=[('PR', 'PRIVATE'), ('PU', 'PUBLIC')], default='PU', max_length=8),
        ),
    ]
