# Generated by Django 3.2.4 on 2021-07-06 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20210706_0008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opsdone',
            name='name',
            field=models.CharField(max_length=255, verbose_name='نام کارگروه'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=255, verbose_name='تگ'),
        ),
    ]
