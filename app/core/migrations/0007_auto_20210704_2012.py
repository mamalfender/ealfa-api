# Generated by Django 3.2.4 on 2021-07-04 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20210704_1932'),
    ]

    operations = [
        migrations.RenameField(
            model_name='animal',
            old_name='Age',
            new_name='age',
        ),
        migrations.RemoveField(
            model_name='animal',
            name='cost_of_ops',
        ),
        migrations.RemoveField(
            model_name='opsdone',
            name='co_ops',
        ),
        migrations.RemoveField(
            model_name='opsdone',
            name='cost',
        ),
        migrations.RemoveField(
            model_name='opsdone',
            name='main_agent',
        ),
        migrations.RemoveField(
            model_name='opsdone',
            name='support',
        ),
        migrations.AddField(
            model_name='animal',
            name='food_cost',
            field=models.IntegerField(default=0, verbose_name='هزینه غذا'),
        ),
        migrations.AddField(
            model_name='animal',
            name='keep_cost',
            field=models.IntegerField(default=0, verbose_name='هزینه نگهداری'),
        ),
        migrations.AddField(
            model_name='animal',
            name='med_cost',
            field=models.IntegerField(default=0, verbose_name='هزینه دارو'),
        ),
        migrations.AddField(
            model_name='animal',
            name='op_cost',
            field=models.IntegerField(default=0, verbose_name='هزینه عمل'),
        ),
        migrations.AddField(
            model_name='animal',
            name='sum_cost',
            field=models.IntegerField(default=0, verbose_name='جمع هزینه ها'),
        ),
        migrations.AddField(
            model_name='animal',
            name='support',
            field=models.CharField(default='ندارد', max_length=255, verbose_name='نام حامی'),
        ),
        migrations.AddField(
            model_name='animal',
            name='visit_cost',
            field=models.IntegerField(default=0, verbose_name='هزینه ویزیت'),
        ),
        migrations.AlterField(
            model_name='animal',
            name='breed',
            field=models.CharField(blank=True, max_length=255, verbose_name='نژاد'),
        ),
        migrations.AlterField(
            model_name='animal',
            name='name',
            field=models.CharField(default='ندارد', max_length=255, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='animal',
            name='opsdone',
            field=models.ManyToManyField(to='core.OpsDone', verbose_name='کارگروه'),
        ),
        migrations.AlterField(
            model_name='animal',
            name='tags',
            field=models.ManyToManyField(to='core.Tag', verbose_name='تگ ها'),
        ),
        migrations.AlterField(
            model_name='opsdone',
            name='name',
            field=models.CharField(default='', max_length=255, verbose_name='نام کارگروه'),
        ),
    ]