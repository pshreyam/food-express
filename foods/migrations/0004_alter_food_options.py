# Generated by Django 3.2 on 2021-05-01 00:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0003_auto_20210426_1114'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='food',
            options={'ordering': ('-created',)},
        ),
    ]
