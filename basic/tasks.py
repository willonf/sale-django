from celery import shared_task
from basic import actions


@shared_task(queue='default')
def sale_by_year_to_a_file():
    # Na prática, toda a lógica deve estar em outro arquivo (managers, actions, etc) e ser invocada aqui
    actions.SaleActions.sale_by_year()
