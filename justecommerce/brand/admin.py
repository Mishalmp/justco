from django.contrib import admin
from .models import brand
# Register your models here.

class brandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('brand_name',)}


admin.site.register(brand,brandAdmin)