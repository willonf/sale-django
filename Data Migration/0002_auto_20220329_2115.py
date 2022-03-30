# Generated by Django 4.0.3 on 2022-03-30 01:15
# Esse arquivo deve estar contido em um módulo de migrations
from django.db import migrations


# TODO: Método para manipulação dos dados
def create_marital_status(apps, schema_editor):
    marital_status_list = ['CASADO', 'SOLTEIRO', 'DIVORCIADO', 'VIÚVO']
    MaritalStatus = apps.get_registered_model(app_label='basic', model_name='MaritalStatus')
    for ms in marital_status_list:
        marital_status = MaritalStatus()
        marital_status.name = ms
        marital_status.save()


# TODO: Classe de migração
class Migration(migrations.Migration):
    # TODO: Migrations dependentes para rodar essa migration
    dependencies = [
        ('basic', '0001_initial'),
    ]

    # TODO: Operações para serem realizadas na migration
    operations = [
        migrations.RunPython(create_marital_status)
    ]

    # TODO: Outra opção de realizar seed ou data migration:
    # operations = [
    #     migrations.RunSQL(
    #         "INSERT INTO marital_status (name, created_at, modified_at, active) VALUES ('Solteiro', current_timestamp, current_timestamp, true );"),
    #     migrations.RunSQL(
    #         "INSERT INTO marital_status (name, created_at, modified_at, active) VALUES ('Casado', current_timestamp, current_timestamp, true );"),
    #     migrations.RunSQL(
    #         "INSERT INTO marital_status (name, created_at, modified_at, active) VALUES ('Divorciado', current_timestamp, current_timestamp, true );"),
    #     migrations.RunSQL(
    #         "INSERT INTO marital_status (name, created_at, modified_at, active) VALUES ('Viúvo', current_timestamp, current_timestamp, true );"),
    # ]
