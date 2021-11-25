# Generated by Django 3.2.8 on 2021-11-24 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='url of node')),
                ('allowIncoming', models.BooleanField()),
                ('allowOutgoing', models.BooleanField()),
                ('authRequiredIncoming', models.BooleanField()),
                ('authRequiredOutgoing', models.BooleanField()),
                ('incomingName', models.CharField(default='defaultName', max_length=128)),
                ('outgoingName', models.CharField(default='defaultName', max_length=128)),
                ('incomingPassword', models.CharField(default='passpass', max_length=128)),
                ('outgoingPassword', models.CharField(default='passpass', max_length=128)),
            ],
        ),
    ]
