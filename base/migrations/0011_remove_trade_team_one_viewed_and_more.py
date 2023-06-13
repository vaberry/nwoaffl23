# Generated by Django 4.2.2 on 2023-06-13 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_rename_team_one_trade_seen_trade_team_one_viewed_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trade',
            name='team_one_viewed',
        ),
        migrations.RemoveField(
            model_name='trade',
            name='team_two_viewed',
        ),
        migrations.AddField(
            model_name='team',
            name='team_new_trade',
            field=models.BooleanField(default=False),
        ),
    ]