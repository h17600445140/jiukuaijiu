# Generated by Django 2.1.2 on 2018-11-21 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goodsid', models.IntegerField()),
                ('colorid', models.IntegerField()),
                ('sizeid', models.IntegerField()),
                ('count', models.IntegerField()),
                ('isdelete', models.BooleanField(default=False)),
            ],
        ),
    ]
