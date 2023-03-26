from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Auto, Owner
from .serializers import AutoSerializer, OwnerSerializer, AutoListSerializer, OwnerListSerializer


class AutoViewsSet(viewsets.ModelViewSet):
    queryset = Auto.objects.all()
    serializer_class = AutoSerializer

    @action(detail=False)
    def multiple_purchase(self, request):
        autos = Auto.objects.annotate(owners_count=Count('owners')).filter(owners_count__gte=1)
        serializer = self.get_serializer(autos, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'list':
            return AutoListSerializer
        return AutoSerializer


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return OwnerListSerializer
        return OwnerSerializer
