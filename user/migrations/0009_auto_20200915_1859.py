# Generated by Django 3.0.8 on 2020-09-15 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20200915_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birthdate',
            field=models.DateField(blank=True, null=True, verbose_name='birth date'),
        ),
    ]
