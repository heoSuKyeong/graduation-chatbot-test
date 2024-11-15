from rest_framework import serializers
from .models import MainCategory, SubCategory

class mainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=MainCategory
        fields='__all__'

class subCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=SubCategory
        fields='__all__'
