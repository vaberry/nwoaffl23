# Generated by Django 4.2.2 on 2023-08-18 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_remove_trade_team_one_viewed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pick',
            name='selection',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
