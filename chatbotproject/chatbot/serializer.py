from rest_framework import serializers
from .models import MainCategory, SubCategory, Product, Aspect, Review, ReviewAspect

class MainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategory
        fields = "__all__"


class SubCategorySerializer(serializers.ModelSerializer):
    main_category = MainCategorySerializer(read_only=True)

    class Meta:
        model = SubCategory
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("main_category", None)
        return representation


class ProductSerializer(serializers.ModelSerializer):
    sub_category = SubCategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("sub_category", None)
        return representation


class AspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aspect
        fields = "__all__"


class ReviewAspectSerializer(serializers.ModelSerializer):
    review = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all())
    aspect = AspectSerializer(read_only=True)

    class Meta:
        model = ReviewAspect
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    review_aspects = ReviewAspectSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = "__all__"