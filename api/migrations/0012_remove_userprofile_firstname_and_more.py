# Generated by Django 4.2.5 on 2023-10-03 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_remove_order_totalprice_userprofile_firstname_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='lastname',
        ),
    ]
