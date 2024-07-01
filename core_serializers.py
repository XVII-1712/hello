from rest_framework import serializers
from .models import LatticeDesign

class LatticeDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatticeDesign
        fields = '__all__'
