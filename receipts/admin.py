from django.contrib import admin
from .models import Ip, Ipdet



class IpdetInline(admin.TabularInline):
    model = Ipdet
    readonly_fields = ('subtotal',)
    extra = 1  # Puedes ajustar esto según tus necesidades


class IpAdmin(admin.ModelAdmin):    
    list_display = ('tipo', 'number', 'total', 'created_date')
    list_display_links = ('tipo', 'number', 'total', 'created_date')
    search_fields = ('number','created_data',)
    readonly_fields = ('total',)
    inlines = [IpdetInline]    
    list_per_page = 6

    def total_en_pesos(self, obj):
        return f'${obj.total:.2f}'
    
admin.site.register(Ip, IpAdmin)
