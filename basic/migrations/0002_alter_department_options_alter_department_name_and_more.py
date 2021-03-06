# Generated by Django 4.0.3 on 2022-03-31 01:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'managed': True, 'verbose_name': 'Department', 'verbose_name_plural': 'Departments'},
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(error_messages={'unique': 'This department already exists.'}, max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(db_column='id_department', on_delete=django.db.models.deletion.DO_NOTHING, related_name='employees', to='basic.department'),
        ),
    ]
