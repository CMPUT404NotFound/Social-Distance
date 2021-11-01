# Generated by Django 3.1.6 on 2021-11-01 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='contentType',
            field=models.CharField(choices=[('P', 'text/plain'), ('M', 'text/markdown')], default='P', max_length=1, verbose_name='contentType'),
        ),
    ]
