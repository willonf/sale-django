from django.db.models import Q
from basic import models

# TODO: Consultas no banco

# O valor armazenado em 'zones' é um QuerySet, uma classe do django cuja função é armazenar consultas.
#  É um iterator. Só é executado quando ocorre alguma operação que utilize o QuerySet
zones = models.Zone.objects.all()
print(zones)  # Aqui a consulta é realizada, pois a operação foi chamada

print(zones.query)  # Exibe a string SQL que ele forma

# Filter: O .filter() cria uma cláusula where na consulta
employee_ana_luiza = models.Employee.objects.filter(
    name='Ana Luiza Cunha')
employee_id_100 = models.Employee.objects.filter(pk=100)
female_employees = models.Employee.objects.filter(gender=models.ModelBase.Gender.FEMALE)
female_employees2 = models.Employee.objects.filter(gender=models.ModelBase.Gender.MALE, salary=2097)

# Ordenação (order by)
ordered_employees_by_salary = models.Employee.objects.order_by('salary')
# ASC. Para DESC coloca-se (-salary). O Django entende que precisa trazer todos.

# Values: diferente dos outros métodos (que retornam um queryset), .values() retorna uma lista de dicionários.
employees3 = models.Employee.objects.values('id', 'name')
# É possível combinar funções: .filter().values()

# As consultas acima utilizam o AND (&). Para usar o OR (|):

qs = models.Employee.objects.filter(Q(name='Silva') | Q(salary=2097))
qs1 = models.Employee.objects.filter(Q(name='Rocha') & Q(salary=2097))

# Utilizando o NOT: No queryset abaixo, serão pesquisados todos os employees que não são do sexo masculino
qs2 = models.Employee.objects.exclude(gender=models.ModelBase.Gender.MALE)
