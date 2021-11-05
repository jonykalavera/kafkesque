# Generated by Django 3.2.5 on 2021-08-01 13:35

import kafkesque.consumers.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WebhookConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('topics', models.CharField(max_length=200)),
                ('serialization_format', models.CharField(choices=[('json', 'JSON'), ('xml', 'XML')], default=kafkesque.consumers.models.SerializationFormat, max_length=100)),
                ('status', models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE')], default=
                kafkesque.consumers.models.WebhookStatus['ACTIVE'], max_length=100)),
                ('ts_expire', models.DateTimeField(blank=True, default=None, null=True)),
                ('batch_size', models.SmallIntegerField(blank=True, default=None, null=True)),
                ('batch_max_interval', models.IntegerField(blank=True, default=None, null=True)),
            ],
        ),
    ]
