from django.contrib import admin
from .models import Tercero

class TerceroAdmin(admin.ModelAdmin):    
    list_display = ('document', 'name', 'addres', 'phone', 'email', 'cust')
    list_display_links = ('document', 'name', 'addres', 'phone', 'email')
    search_fields = ('document', 'name', 'addres', 'phone', 'email',)   
    list_per_page = 10
    
admin.site.register(Tercero, TerceroAdmin)
