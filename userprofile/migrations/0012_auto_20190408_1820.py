# Generated by Django 2.0.13 on 2019-04-08 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0011_auto_20190321_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='social_battlenet',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='social_discord',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='social_git',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='social_slack',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='social_steam',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
