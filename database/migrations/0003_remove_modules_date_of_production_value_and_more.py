# Generated by Django 5.1.1 on 2024-10-30 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_modules_date_of_production_value_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modules',
            name='date_of_production_value',
        ),
        migrations.RemoveField(
            model_name='modules',
            name='history_of_module_value',
        ),
        migrations.RemoveField(
            model_name='modules',
            name='manufacturer_value',
        ),
        migrations.RemoveField(
            model_name='modules',
            name='number_ec_value',
        ),
        migrations.RemoveField(
            model_name='modules',
            name='product_family_value',
        ),
        migrations.RemoveField(
            model_name='modules',
            name='product_type_value',
        ),
        migrations.RemoveField(
            model_name='modules',
            name='revision_value',
        ),
        migrations.RemoveField(
            model_name='modules',
            name='sequence_number_value',
        ),
        migrations.RemoveField(
            model_name='modules',
            name='serial_number_value',
        ),
    ]
