from django.contrib import admin
from .models import Product, ProductVariant, ProductVariantPrice, ProductImage, Variant

admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(ProductVariantPrice)
admin.site.register(Variant)
admin.site.register(ProductImage)
# Register your models here.
