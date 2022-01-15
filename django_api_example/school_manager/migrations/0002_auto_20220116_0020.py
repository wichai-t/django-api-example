# Generated by Django 3.2 on 2022-01-15 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_manager', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='name',
        ),
        migrations.AlterField(
            model_name='school',
            name='max_student',
            field=models.IntegerField(default=3000, verbose_name='Maximum number of student'),
        ),
    ]
