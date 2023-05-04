# Generated by Django 4.1.7 on 2023-04-29 15:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='watchlist_name', to=settings.AUTH_USER_MODEL),
        ),
    ]
