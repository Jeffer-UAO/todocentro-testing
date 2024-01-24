from django.contrib import admin
from ips.models import Ip

@admin.register(Ip)
class IpAdmin(admin.ModelAdmin):
    list_display = ['number', 'tipo']
