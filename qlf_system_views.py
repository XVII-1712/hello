from rest_framework import viewsets
from .models import LatticeDesign, Application
from .serializers import LatticeDesignSerializer, ApplicationSerializer

class LatticeDesignViewSet(viewsets.ModelViewSet):
    queryset = LatticeDesign.objects.all()
    serializer_class = LatticeDesignSerializer

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
