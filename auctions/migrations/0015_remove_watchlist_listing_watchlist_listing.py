# Generated by Django 4.0.4 on 2022-10-03 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_remove_watchlist_added'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='listing',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='listing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
    ]