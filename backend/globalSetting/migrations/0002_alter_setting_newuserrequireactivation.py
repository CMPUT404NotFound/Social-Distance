# Generated by Django 3.2.8 on 2021-11-25 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('globalSetting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='newUserRequireActivation',
            field=models.BooleanField(default=False, verbose_name='New User Require Activation'),
        ),
    ]
