# from django.contrib import admin
# from .models import DocumentOut, DocumentEntry, ProductEntry, ProductOut, WarehomeDetail, Stock


# # -------------------

# class ProductEntryDetailInline(admin.TabularInline):
#     readonly_fields = ('ProductEntry', 'ProductOut')
#     model = WarehomeDetail

# # ------------------------


# class DocumentEntryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'type', 'description')
#     list_display_links = ('id', 'type', 'description')
#     search_fields = ('type',)
#     list_per_page = 12


# class DocumentOutAdmin(admin.ModelAdmin):
#     list_display = ('id', 'type', 'description')
#     list_display_links = ('id', 'type', 'description')
#     search_fields = ('type',)
#     list_per_page = 12


# class ProductEntryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'number', 'customer',
#                     'created_date', 'deudate', 'comments')
#     list_display_links = ('id', 'number', 'customer')
#     search_fields = ('id', 'number')
#     list_per_page = 5
#     inlines = [ProductEntryDetailInline]


# class ProductOutAdmin(admin.ModelAdmin):
#     list_display = ('number', 'user',
#                     'created_date', 'deudate', 'comments')
#     list_display_links = ('number', 'user')
#     search_fields = ('number', 'user')
#     list_per_page = 5
#     inlines = [ProductEntryDetailInline]


# class StockAdmin(admin.ModelAdmin):
#     def get_readonly_fields(self, request, obj=None):
#         actions = super(Stock, self).get_actions(request)
#         return ['product_id', 'qty']
#     actions= None
#     list_display = ('product_id', 'qty', 'attribut', 'description')
#     search_fields = ('product_id',)
#     list_display_links = None
#     list_per_page = 8


# # ------------------------

# admin.site.register(ProductEntry, ProductEntryAdmin)
# admin.site.register(ProductOut, ProductOutAdmin)
# admin.site.register(DocumentEntry, DocumentEntryAdmin)
# admin.site.register(DocumentOut, DocumentOutAdmin)
# admin.site.register(Stock, StockAdmin)


# # ------------------------
