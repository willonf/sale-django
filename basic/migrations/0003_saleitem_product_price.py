# Generated by Django 4.0.3 on 2022-05-11 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0002_alter_department_options_alter_department_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleitem',
            name='product_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=16),
        ),
    ]
