# Generated by Django 5.1.3 on 2024-11-19 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_remove_modules_date_of_production_value_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='modules',
            name='module_id',
            field=models.CharField(default=1, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
