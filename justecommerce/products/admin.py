from django.contrib import admin
from .models import Product,PriceFilter,Variations,Color
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}



admin.site.register(Product,ProductAdmin)

admin.site.register(PriceFilter)
admin.site.register(Variations)
admin .site.register(Color)