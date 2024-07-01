from rest_framework import serializers
from .models import LatticeDesign, Application

class LatticeDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatticeDesign
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
