from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Script
from .serializers import ScriptSerializer


class ScriptViewSet(viewsets.ModelViewSet):
    queryset = Script.objects.all()
    serializer_class = ScriptSerializer
