# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 12, 5, 7, 57, 7, 360733, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photo',
            name='description',
            field=models.TextField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photo',
            name='image',
            field=models.ImageField(default='', upload_to='%Y/%m/%d/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photo',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 5, 7, 57, 46, 626693, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photo',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=False,
        ),
    ]
