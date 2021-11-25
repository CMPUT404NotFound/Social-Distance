# Generated by Django 3.2.8 on 2021-11-25 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0009_alter_comment_contenttype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='contentType',
            field=models.CharField(choices=[('M', 'text/markdown'), ('P', 'text/plain')], default='P', max_length=1, verbose_name='contentType'),
        ),
    ]
