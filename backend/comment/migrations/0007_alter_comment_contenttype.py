# Generated by Django 3.2.8 on 2021-10-29 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0006_auto_20211029_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='contentType',
            field=models.CharField(choices=[('P', 'text/plain'), ('M', 'text/markdown')], default='P', max_length=1, verbose_name='contentType'),
        ),
    ]
