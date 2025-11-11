from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.renderers import JSONRenderer

from .models import Incident
from .serializers import IncidentSerializer


class IncidentViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Incident.objects.all()
    renderer_classes = [JSONRenderer]
    serializer_class = IncidentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]
