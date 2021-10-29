# Generated by Django 3.1.6 on 2021-10-29 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20211028_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='visibility',
            field=models.CharField(choices=[('PR', 'PRIVATE'), ('PU', 'PUBLIC')], default='PU', max_length=8),
        ),
        migrations.AlterField(
            model_name='postsmanager',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]