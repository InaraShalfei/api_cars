import datetime

from django.db.models import Count, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Auto, Owner
from .serializers import AutoSerializer, OwnerSerializer, AutoListSerializer, OwnerListSerializer


class AutoViewsSet(viewsets.ModelViewSet):
    queryset = Auto.objects.all()
    serializer_class = AutoSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('model', 'color', 'production_year')
    search_fields = ('^model', )

    @action(detail=False)
    def multiple_purchase(self, request):
        autos = Auto.objects.annotate(owners_count=Count('owners')).filter(owners_count__gte=1)
        serializer = AutoListSerializer(autos, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'list':
            return AutoListSerializer
        return AutoSerializer


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('first_name', 'last_name', 'date_of_birth', 'nationality')
    search_fields = ('^first_name', '^last_name',)

    @action(detail=False)
    def adults(self, request):
        current_time = datetime.datetime.now()
        current_year_int = int(current_time.strftime('%Y'))
        owners = Owner.objects.annotate(difference=current_year_int - F('date_of_birth')).filter(difference__gte=18)
        serializer = OwnerListSerializer(owners, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'list':
            return OwnerListSerializer
        return OwnerSerializer
