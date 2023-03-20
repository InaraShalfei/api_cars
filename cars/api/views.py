from rest_framework import viewsets

from .models import Auto, Owner
from .serializers import AutoSerializer, OwnerSerializer


class AutoViewsSet(viewsets.ModelViewSet):
    queryset = Auto.objects.all()
    serializer_class = AutoSerializer


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
