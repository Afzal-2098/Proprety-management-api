from rest_framework import serializers
from .models import PropertyDetail

# Serialize the PropertyDetail data
class PropertyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyDetail
        fields = '__all__'