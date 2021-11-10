# Generated by Django 3.2.8 on 2021-11-10 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_alter_post_contenttype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='contentType',
            field=models.CharField(choices=[('png', 'image/png;base64'), ('app', 'application/base64'), ('plain', 'text/plain'), ('jpeg', 'image/jpeg;base64'), ('markdown', 'text/markdown')], default='plain', max_length=20),
        ),
    ]