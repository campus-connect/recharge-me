# Generated by Django 2.2.2 on 2019-06-22 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20190620_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='level',
            name='order',
            field=models.PositiveSmallIntegerField(default=None),
            preserve_default=False,
        ),
    ]
