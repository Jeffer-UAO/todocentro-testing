from django.contrib import admin
from ips.models import Ip, Ipdet



class IpdetInline(admin.TabularInline):
    model = Ipdet
    extra = 1  # Puedes ajustar esto según tus necesidades


class IpAdmin(admin.ModelAdmin):    
    actions= None
    list_display = ('tipo', 'number', 'total', 'created_date')
    search_fields = ('number','created_data')
    inlines = [IpdetInline]
    list_display_links = None
    list_per_page = 8
    
admin.site.register(Ip, IpAdmin)
