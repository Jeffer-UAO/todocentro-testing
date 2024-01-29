from django.contrib import admin
from .models import Order, Orderdet


class IpdetInline(admin.TabularInline):
    model = Orderdet
    readonly_fields = ('subtotal',)
    extra = 1  # Puedes ajustar esto según tus necesidades


class IpAdmin(admin.ModelAdmin):    
    list_display = ('tipo', 'number', 'total', 'created_date')
    list_display_links = ('tipo', 'number', 'total', 'created_date')
    search_fields = ('number','created_data',)
    readonly_fields = ('total',)
    inlines = [IpdetInline]    
    list_per_page = 6
    
admin.site.register(Order, IpAdmin)
