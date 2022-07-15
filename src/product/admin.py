from django.contrib import admin
from .models import Product, ProductVariant, ProductVariantPrice, ProductImage, Variant


class ProductAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant)
admin.site.register(ProductVariantPrice)
admin.site.register(Variant)

# Register your models here.
