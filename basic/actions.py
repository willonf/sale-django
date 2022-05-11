from basic import models


class SaleActions:
    @staticmethod
    def sale_by_year():
        results = models.SaleItem.objects.sold_by_year()
        results = map(lambda item: f"{item['year']} - R$ {item['subtotal']};\n", results)
        with open('sale_by_year.txt', 'a') as file:
            file.writelines(results)
