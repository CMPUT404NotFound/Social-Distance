# Generated by Django 3.2.8 on 2021-10-29 21:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=200, primary_key=True, serialize=False)),
                ('displayName', models.CharField(blank=True, default='', max_length=40)),
                ('userName', models.CharField(default='defaultName', max_length=40, unique=True, verbose_name='userName')),
                ('github', models.URLField(blank=True, max_length=60, verbose_name='github')),
                ('profileImage', models.URLField(blank=True, verbose_name='profileImage')),
                ('is_admin', models.BooleanField(default=False)),
                ('isLocalUser', models.BooleanField(default=True)),
                ('host', models.URLField(blank=True, default='')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
