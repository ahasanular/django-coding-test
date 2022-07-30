from rest_framework import serializers
from .models import Product, ProductVariant, ProductVariantPrice


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['variant_title']


class ProductVariantPriceSerializer(serializers.ModelSerializer):
    product_variant_one = ProductVariantSerializer()
    product_variant_two = ProductVariantSerializer()
    product_variant_three = ProductVariantSerializer()

    class Meta:
        model = ProductVariantPrice
        fields = ['product_variant_one', 'product_variant_two', 'product_variant_three', 'price', 'stock']


# class ProductAllDetailsSerializer(serializers.ModelSerializer):
#     productVariantPrice = ProductVariantPriceSerializer(many=True)
#     productVariant = ProductVariantSerializer(many=True)
#
#     class Meta:
#         fields = ['productVariantPrice', 'productVariant']


class ProductSerializer(serializers.ModelSerializer):
    productVariantPrice = ProductVariantPriceSerializer(many=True)
    # productVariant = ProductVariantSerializer(many=True)
    # ProductAllDetails = ProductAllDetailsSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'created_at', 'productVariantPrice']
