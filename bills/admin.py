from django.contrib import admin
from .models import Oe, Oedet, Orderdet


class OrderdetInline(admin.TabularInline):
    model = Orderdet
    extra = 1

class OedetInline(admin.TabularInline):
    model = Oedet
    readonly_fields = ('subtotal',)
    extra = 0  # Puedes ajustar esto según tus necesidades


class OeAdmin(admin.ModelAdmin):    
    list_display = ('tipo', 'number', 'total', 'created_date')
    list_display_links = ('tipo', 'number', 'total', 'created_date')
    search_fields = ('number','created_data',)
    readonly_fields = ('total',)
    inlines = [OedetInline, OrderdetInline]    
    list_per_page = 6
    
admin.site.register(Oe, OeAdmin)