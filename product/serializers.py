from rest_framework import serializers
from django.db.models import Avg
from .models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError(
                "Название категории слишком короткое"
            )
        return value



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'category']

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Название товара минимум 3 символа"
            )
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Цена должна быть больше 0"
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product', 'product_id']

    def validate_text(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Отзыв слишком короткий"
            )
        return value

    def validate_stars(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Оценка должна быть от 1 до 5"
            )
        return value

    def create(self, validated_data):
        product_id = validated_data.pop('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError(
                {"product_id": "Товар не найден"}
            )

        return Review.objects.create(product=product, **validated_data)



class ProductReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'reviews', 'rating']

    def get_rating(self, obj):
        avg = obj.reviews.aggregate(avg=Avg('stars'))['avg']
        return round(avg, 1) if avg else 0


class CategoryCountSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']
