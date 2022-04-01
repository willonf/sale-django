from rest_framework import viewsets
from basic import models, serializers


class EmployeeViewSet(viewsets.ModelViewSet):
    # O queryset abaixo é padrão, mas podemos adicionar outro queryset nesse endpoint
    # ou sobrescrever o método padrão list():
    #     def list(self, request, *args, **kwargs):
    #         self.queryset = queries.minhaquery()

    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer
