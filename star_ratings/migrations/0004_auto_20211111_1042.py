# Generated by Django 3.2.8 on 2021-11-11 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('star_ratings', '0003_auto_20160721_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='userrating',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
