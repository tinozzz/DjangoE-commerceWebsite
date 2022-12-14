# Generated by Django 4.0.4 on 2022-10-03 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_comment_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='added',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
    ]
