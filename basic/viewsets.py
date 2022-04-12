from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as django_filter
from basic import models, serializers, serializers_params, queries, serializers_results, filters


# TODO: Métodos padrões do viewset. Podem ser sobrescritos

class ExampleBranchViewSet(viewsets.ModelViewSet):
    queryset = models.Branch.objects.all()
    serializer_class = serializers.BranchSerializer

    def create(self, request, *args, **kwargs):  # Post
        return super(ExampleBranchViewSet, self).create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):  # Patch
        return super(ExampleBranchViewSet, self).partial_update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):  # Get
        return super(ExampleBranchViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):  # Get/{param}
        return super(ExampleBranchViewSet, self).retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):  # Delete
        return super(ExampleBranchViewSet, self).destroy(request, *args, **kwargs)


class BranchViewSet(viewsets.ModelViewSet):
    # O queryset abaixo é padrão, mas podemos adicionar outro queryset nesse endpoint
    # ou sobrescrever o métodos padrões, como o list():
    #     def list(self, request, *args, **kwargs):
    #         self.queryset = queries.minhaquery()

    queryset = models.Branch.objects.all()
    serializer_class = serializers.BranchSerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = models.City.objects.all()
    serializer_class = serializers.CitySerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = models.District.objects.all()
    serializer_class = serializers.DistrictSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer

    # O ideal é que não haja processamento envolvendo regras de negócio no viewset
    # O ideal é colocar isso em outro lugar (actions, behaviors, models, etc)
    @action(detail=True, methods=['PATCH'])
    def increase_salary(self, request, *args, **kwargs):
        # print(self.get_object())  # TODO: self.get_object() retorna o objeto do detail
        param_serializer = serializers_params.EmployeeParamsSerializer(data=request.data)
        print(self.get_object().salary)
        if param_serializer.is_valid(raise_exception=True):
            employee = self.get_object()
            employee.increase_salary(param_serializer.validated_data['increase'])
            print(employee.salary)
            employee.save()
            result = self.get_serializer(instance=employee, context=self.get_serializer_context())
            return Response(data=result.data, status=200)


class MaritalStatusViewSet(viewsets.ModelViewSet):
    queryset = models.MaritalStatus.objects.all()
    serializer_class = serializers.MaritalStatusSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


class ProductGroupViewSet(viewsets.ModelViewSet):
    queryset = models.ProductGroup.objects.all()
    serializer_class = serializers.ProductGroupSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = models.Sale.objects.all()
    serializer_class = serializers.SaleSerializer


class SaleItemViewSet(viewsets.ModelViewSet):
    queryset = models.SaleItem.objects.all()
    serializer_class = serializers.SaleItemSerializer

    @action(methods=['GET'], detail=False)
    def sold_by_year(self, request, *args, **kwargs):
        # queryset = queries.total_sold_by_year()
        # Também pode ser chamado do manager:
        queryset = models.SaleItem.objects.sold_by_year()
        serialized_queryset = serializers_results.SoldByYearSerializer(instance=queryset, many=True,
                                                                       context=self.get_serializer_context())
        return Response(data=serialized_queryset.data, status=200)


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = models.Supplier.objects.all()
    serializer_class = serializers.SupplierSerializer


class StateViewSet(viewsets.ModelViewSet):
    queryset = models.State.objects.all()
    serializer_class = serializers.StateSerializer


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = models.Zone.objects.all()
    serializer_class = serializers.ZoneSerializer
    filter_class = filters.ZoneFilter
    ordering = ('-id',)
    # Para ordenar qualquer campo na url: .../zone/?ordering=-name ou .../zone/?ordering=name
    ordering_fields = '__all__'
    # OBS.: os orderings são usados na queryset padrão (linha 125, nesse caso) do viewset

    @action(detail=False, methods=['GET'])
    def get_zone_by_name1(self, request, *args, **kwargs):
        result = serializers_params.ZoneParamsSerializer(data=request.query_params, context={'request': request})
        result.is_valid(raise_exception=True)
        self.queryset = self.get_queryset().filter(name__icontains=result.validated_data['name'])
        return super(ZoneViewSet, self).list(request, *args, **kwargs)

    @action(detail=False, methods=['GET'])
    # Detail: False (o endpoint não é baseado em um objeto específico)
    # Detail: True (o endpoint é específico, geralmente, para o registro associado na URL: .../zone/1/change_area/)
    def get_zone_by_name2(self, request, *args, **kwargs):
        # Body request: request.data | Query parameters request: request.query_params
        # name = request.query_params['name']  ou name = request.query_params.get('name')

        # TODO: Os parâmetros devem ser serializados!
        param_serializer = serializers_params.ZoneParamsSerializer(data=request.query_params)
        if param_serializer.is_valid(raise_exception=True):
            # FORMA 1:
            queryset = self.queryset.filter(name__icontains=param_serializer.data['name'])
            # queryset = self.get_queryset().filter(name__icontains=name)  # Outra forma

            # Serializando a busca do queryset:
            # many=True: usado para serializar um queryset ou lista de objetos
            result = serializers.ZoneSerializer(instance=queryset, many=True, context=self.get_serializer_context())
            # Outra forma
            # result = self.get_serializer(instance=queryset, many=False, context=self.get_serializer_context())
            return Response(data=result.data, status=200)
            # FORMA 2:
            # return super(ZoneViewSet, self).list(request, *args, **kwargs)
        return Response(data=param_serializer.errors, status=400)
        # TODO: Response error personalizado (tem que tirar o raise_exception=True)
        # return Response(data=data={'Erro!'}, status=400)
