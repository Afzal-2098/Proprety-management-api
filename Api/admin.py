from django.contrib import admin
from .models import PropertyDetail

# Register your models here.
@admin.register(PropertyDetail)
class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ["id", "property_name", "address", "city", "state"]