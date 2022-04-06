from django.db.models import (
    Q, IntegerField, Sum, ExpressionWrapper, F, FloatField, Count, Value, When, Case,
    DateField, DurationField, Func)
from django.db.models.functions import Extract, Now, Cast, ExtractDay, ExtractYear

from basic import models


# TODO: Consultas no banco
# O valor armazenado em 'zones' é um QuerySet, uma classe do django cuja função é armazenar consultas.
#  É um iterator. Só é executado quando ocorre alguma operação que utilize o QuerySet


def all_zones():
    zones = models.Zone.objects.all()
    print(zones)  # Aqui a consulta é realizada, pois a operação foi chamada
    print(zones.query)  # Exibe a string SQL que ele forma
    return zones


# Filter: O .filter() cria uma cláusula where na consulta
def ana_luiza():
    return models.Employee.objects.filter(name='Ana Luiza Cunha')


def employee_id_100():
    return models.Employee.objects.filter(pk=100)


def female_employees():
    return models.Employee.objects.filter(gender=models.ModelBase.Gender.FEMALE)


def female_employees2():
    return models.Employee.objects.filter(gender=models.ModelBase.Gender.MALE, salary=2097)


# Ordenação (order by)
def ordered_employees_by_salary():
    models.Employee.objects.order_by('salary')
    # ASC. Para DESC coloca-se (-salary). O Django entende que precisa trazer todos.


# Values: diferente dos outros métodos (que retornam um queryset), .values() retorna uma lista de dicionários.
def employees_id_name():
    return models.Employee.objects.values('id', 'name')


# É possível combinar funções: .filter().values()

# As consultas acima utilizam o AND (&). Para usar o OR (|) utilizamos o Q:

def employee_filter1():
    return models.Employee.objects.filter(Q(name='Silva') | Q(salary=2097))


def employee_filter2():
    return models.Employee.objects.filter(Q(name='Rocha') & Q(salary=2097))


# Outra forma é criarmos um objeto Q e na query passarmos como parâmetro

def employee_filter3():
    conditions = Q()
    conditions.add(Q(salary__gte=1000), Q.AND)
    conditions.add(Q(name='Rocha'), Q.AND)
    return models.Employee.objects.filter(conditions)


# Utilizando o NOT na cláusula WHERE:
# No queryset abaixo, serão pesquisados todos os employees que não são do sexo masculino
def employee_filter4():
    return models.Employee.objects.exclude(gender=models.ModelBase.Gender.MALE)


# TODO: Consultas com fields lookups


def employee_salary_gte_1000():
    return models.Employee.objects.filter(salary__gte=1000)  # __gte: Greater than or equal


def employee_name_icontains_silva():
    return models.Employee.objects.filter(name__icontains='Silva')


# GET: retorna um objeto ao invés de um queryset. Sempre deve retornar um valor único. Lança excessão, usar try catch
def employee_pk_1():
    try:
        models.Department.objects.get(pk=1)
    except models.Employee.DoesNotExist:
        print('Register not found')


# Exercício 1: Todos os funcionários que contenham silva no nome:
def exercicio1():
    return models.Employee.objects.filter(name__icontains='Silva')


# Exercício 2: Todos os funcionários com o salário maior que R$5.000,00
def exercicio2():
    return models.Employee.objects.filter(salary__gt=5000)


# Exercício 3: Todos os clientes que tem uma renda mensal inferior a R$2.000,00
def exercicio3():
    return models.Customer.objects.filter(income__lt=2000)  # __lte: Less than


# Exercício 4: Todos os funcionários admitidos entre 2010 e 2021

def exercicio4():
    return models.Employee.objects.filter(
        admission_date__year__gte=2010, admission_date__year__lte=2021
    ).order_by(
        'admission_date'
    )


# Exercício 4.1: Todos os funcionários admitidos entre 2010 e 2021
def exercicio5():
    return models.Employee.objects.annotate(
        year=Extract(expression='admission_date', lookup_name='year', output_field=IntegerField())
    ).filter(
        year__range=(2010, 2021)
    ).order_by('year')


# Count: retorna um valor inteiro
def employee_count():
    return models.Employee.objects.count()


def employee_filter_count():
    return models.Employee.objects.filter(gender=models.ModelBase.Gender.FEMALE).count()


# Exists: retorna True ou False, ou seja, se existem resultados na consulta
def employee_exists():
    return models.Employee.objects.filter(gender=models.ModelBase.Gender.MALE).exists()


# First e last: traz o primeiro e último objeto do queryset
def employee_first():
    return models.Employee.objects.filter(gender=models.ModelBase.Gender.MALE).first()


def employee_last():
    return models.Employee.objects.filter(gender=models.ModelBase.Gender.MALE).last()


# Exercício 5: Criar uma consulta para trazer o total de funcionários por estado civil
def funcionarios_por_estado_civil():
    return models.Employee.objects.values('marital_status__name').annotate(
        marital_status=F('marital_status__name'),
        total=Count(F('id'))
    ).values('marital_status', 'total')


# Exercício 6: Criar uma consulta para trazer o total vendido em valor R$ por filial;
def exercicio6():
    return models.SaleItem.objects.select_related(
        'sale__branch'
    ).values(
        'sale__branch__name'
    ).annotate(
        total=Sum(ExpressionWrapper(
            F('quantity') * F('product__sale_price'), output_field=FloatField()
        ))
    ).values('sale__branch__name', 'total')


# UPDATE
def employee_update1():
    return models.Employee.objects.filter(gender=models.ModelBase.Gender.FEMALE).update(active=False)


def employee_update2():
    return models.Employee.objects.filter(gender=models.ModelBase.Gender.FEMALE).update(active=True)


# DELETE
def employee_delete():
    return models.Employee.objects.filter(gender=models.ModelBase.Gender.FEMALE).delete()


# Criação de colunas dinâmicas
# Value: usado para colocarmos valores dentro da query
# ExpressionWrapper: utilizado para cálculos dentro da query. Não esquecer de passar o output field
# F: quando queremos usar um field da tabela

def employee_dynamic_field1():
    return models.Employee.objects.annotate(column=Value(10)).values('id', 'name', 'column')


def employee_dynamic_field2():
    return models.Employee.objects.annotate(
        new_salary=ExpressionWrapper(Value(10) + Value(10), output_field=FloatField()))


def employee_dynamic_field3():
    return models.Employee.objects.annotate(
        new_salary=ExpressionWrapper(Value(10) + F('salary'), output_field=FloatField())
    ).values('salary', 'new_salary')


# Exercício 7: Query para retornar o nome do funcionário, o salário atual e salário + 10%
def exercicio7():
    return models.Employee.objects.annotate(
        new_salary=ExpressionWrapper(F('salary') * Value(1.10), output_field=FloatField())
    ).values('name', 'salary', 'new_salary')


# CASE: estruturas condicionais
def employee_case1():
    return models.Employee.objects.annotate(
        gender_description=Case(
            When(gender=models.ModelBase.Gender.MALE, then=Value('Masculino')),
            default=Value('Feminino'))
    ).values('name', 'gender', 'gender_description')


# Exercício 8: Consulta para retornar um status do funcionário de acordo com o seu salário

def exercicio8():
    return models.Employee.objects.annotate(
        status=Case(
            When(salary__lte=2000, then=Value('Vendedor Jr.')),
            When(Q(salary__gt=2000) & Q(salary__lte=5000), then=Value('Vendedor Pleno')),
            default=Value('Vendedor Sênior')
        )
    ).values('name', 'salary', 'status')


# JOINS: Utiliza-se "apenas" dois underlines (__)

def employee_join_department():
    return models.Employee.objects.values('name', 'department', 'department__name')


def employee_join_department_district_city_state1():
    return models.Employee.objects.values('name', 'district__name', 'district__city__name',
                                          'district__city__state__name')


def employee_join_department_district_city_state2():
    return models.Employee.objects.annotate(
        bairro=F('district__name'), cidade=F('district__city__name'),
        estado=F('district__city__state__name')
    ).values('name', 'bairro', 'cidade', 'estado')


def employee_join_department_district_city_state3():
    return models.Employee.objects.values(
        'name', 'district__name', 'district__city__name', 'district__city__state__name')


def employee_join_filter():
    return models.Employee.objects.filter(department__name='Policial federal')


# Join com relação inversa
def department_employees_salary():
    return models.Department.objects.filter(employees__salary__gte=10000)


# Exercício 9: método que receba como param a quantidade de produtos que serão vendidos e retorne uma consulta quanto
# o funcionário irá ganhar de comissão em cada produto
def exercicio9(quantity):
    # Outra solução:
    # return models.Product.objects.annotate(
    #     subtotal=ExpressionWrapper(F('sale_price') * quantity, output_field=FloatField())
    # ).annotate(
    #     comission=ExpressionWrapper((F('subtotal') * F('product_group__commission_percentage') / 100),
    #                                 output_field=FloatField())
    # ).values('name', 'sale_price', 'subtotal', 'product_group__commission_percentage', 'comission')

    # Obs: Na query acima, toda a expressão de 'subtotal' do annotate será chamado novamente em 'comission'
    # Isso não impacta na performance, pois no banco de dados o plano de execução de query para subtotal já terá sido
    # formado e na próxima vez que 'subtotal' for chamado, isso será mais rápido

    return models.Product.objects.annotate(
        comissao=(Value(quantity) * F('sale_price') * F('product_group__commission_percentage')) / Value(100)
    ).values(
        'name', 'comissao', 'sale_price', 'product_group__commission_percentage')


# Exercício 10: fazer uma consulta para retornar todos os funcionários casados ou solteiros
def exercicio10():
    conditions = Q()
    conditions.add(Q(marital_status__name='Solteiro'), Q.OR)
    conditions.add(Q(marital_status__name='Casado'), Q.OR)
    # Outras formas:
    # return models.Employee.objects.filter(
    #     Q(marital_status__name__icontains='Casado') | Q(marital_status__name__icontains='Solteiro')
    # ).values('name', 'marital_status__name')
    #
    # return models.Employee.objects.filter(
    #     marital_status__name__in=['Solteiro', 'Casado']
    # ).values('name', 'marital_status__name')

    return models.Employee.objects.filter(conditions).values('name', 'marital_status__name')


# Exercício 12: Fazer uma consulta para retornar todos os funcionários que ganham entre R$1000 e R$5000
def exercicio12():
    # return models.Employee.objects.filter(salary__range=(1000, 5000)).values('name', 'salary')
    return models.Employee.objects.filter(Q(salary__gte=1000) & Q(salary__lte=5000)).values('name', 'salary')


# Exercício 13: Fazer uma consulta que retorne a diferença do preço de custo e preço de venda dos produtos;
def exercicio13():
    return models.Product.objects.annotate(
        profit=ExpressionWrapper(F('sale_price') - F('cost_price'), output_field=FloatField())
    ).values(
        'name', 'sale_price', 'cost_price', 'profit'
    )


# Exercício 14: Fazer uma consulta para retornar todos os funcionários que não tenham salário entre R$4000 e R$8000
def exercicio14():
    conditions = Q()
    conditions.add(Q(salary__gte=4000), Q.AND)
    conditions.add(Q(salary__lte=8000), Q.AND)
    return models.Employee.objects.exclude(conditions).values('name', 'salary')


# Exercício 15: Fazer uma consulta para retornar todas as vendas dentre 2010 e 2021
def exercicio15():
    return models.Sale.objects.filter(
        Q(date__year__gte=2010) & Q(date__year__lte=2021)
    ).values(
        'id', 'date'
    )


# Exercício 16: Fazer uma consulta que retorne o tipo de funcionário de acordo com sua idade:
#   18 - 25: Jr. | 26 - 34: Pl. | 35 ou mais: Sr.
def exercicio16():
    # Outra forma:
    # Usando func: o func executa uma função que tem no database, mas não tem no Django
    # Obs.: Incompleto
    #
    # return models.Employee.objects.annotate(
    #     age=ExtractYear(Func(F('birth_date'), function='age', output_field=DurationField()))
    # ).values('name', 'age', 'birth_date')

    return models.Employee.objects.annotate(
        diff=ExpressionWrapper(Cast(Now(), output_field=DateField()) - F('birth_date'), output_field=DurationField()),
        age=ExpressionWrapper(ExtractDay('diff') / 365, output_field=IntegerField()),
        status=Case(
            When(age__range=(18, 25), then=Value('Vendedor Jr.')),
            When(age__range=(26, 34), then=Value('Vendedor Pleno')),
            When(age__gte=35, then=Value('Vendedor Sênior')),
            default=Value('Não identificado')
        )
    ).values('name', 'age', 'status')


# Exercício 17: fazer uma consulta para retornar um status para o funcionário de acordo com o tempo de casa:
#   Até 2 anos: Novato | Acima de 2 e menor ou igual a 5 anos: Intermediário | Acima de 5 anos: Veterano
def exercicio17():
    return models.Employee.objects.annotate(
        diff=ExpressionWrapper(Cast(Now(), output_field=DateField()) - F('admission_date'),
                               output_field=DurationField()),
        work_age=ExpressionWrapper(ExtractDay('diff') / 365, output_field=IntegerField()),
        status=Case(
            When(work_age__lte=2, then=Value('Novato')),
            When(work_age__range=(3, 5), then=Value('Intermediário')),
            When(work_age__gt=5, then=Value('Veterano')),
            default=Value('Não identificado')
        )
    ).values('name', 'work_age', 'status')
