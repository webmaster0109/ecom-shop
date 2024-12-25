from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'created_at', 'updated_at']
    search_fields = ['name', 'price']
    list_filter = ['created_at', 'updated_at']
    list_per_page = 10
    list_max_show_all = 100
    date_hierarchy = 'created_at'
    ordering = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    prepopulated_fields = {'slug': ('name',)}