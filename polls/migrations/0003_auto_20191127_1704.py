# Generated by Django 2.2.7 on 2019-11-27 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20191127_1702'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='pub_date',
            new_name='created_at',
        ),
    ]