# Generated by Django 2.1.2 on 2018-12-04 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='trade_no',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
