from django.contrib import admin
from ips.models import Ip, Ipdet



class IpdetInline(admin.TabularInline):
    model = Ipdet
    extra = 1  # Puedes ajustar esto según tus necesidades

@admin.register(Ip)
class IpAdmin(admin.ModelAdmin):
    inlines = [IpdetInline]
