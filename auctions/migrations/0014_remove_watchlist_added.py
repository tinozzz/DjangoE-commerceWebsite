# Generated by Django 4.0.4 on 2022-10-03 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_watchlist_added_alter_bid_listing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='added',
        ),
    ]
