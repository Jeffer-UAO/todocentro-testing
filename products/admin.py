from django.contrib import admin
import re
from django.urls.resolvers import URLPattern
from django.shortcuts import render
from django.urls import path
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from .models import Product, Category, CategoryProduct, Gallery, Attribut


# ------------------------------------------
# admin.site.index_title = 'Panel Administrativo'
# admin.site.site_header = 'Tienda Virtual NACIOTEX'
# admin.site.site_title = 'Dashboard'
# ------------------------------------------


class GalleryInline(admin.TabularInline):
    model = Gallery

class CategoryProductInline(admin.TabularInline):
    model = CategoryProduct


# class AttributProductInline(admin.TabularInline):
#     model = AttributProduct

# ---------------------------------------------


class AttributAdmin(admin.ModelAdmin):
    list_display = ("name",)
    # inlines = [AttributProductInline]




class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "name_extend",
        "ref",
        "qty",
        "price1",
        "price2",
        "active",
        "soldout",
        "offer",
        "home",
        "flag",
    )
    prepopulated_fields = {"slug": ("flag", "name_extend")}
    list_display_links = ("codigo", "flag", "name_extend")
    search_fields = ("codigo", "flag", "ref", "name_extend")
    ordering = ("name_extend",)
    inlines = [CategoryProductInline, GalleryInline]

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("upload-csv/", self.upload_csv),
        ]
        return new_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES.get("csv_upload")

            if csv_file:
                try:
                    file_data = csv_file.read().decode("utf-8")
                    csv_data = file_data.split("\n")

                    for i, row in enumerate(csv_data):
                        if i == 0:
                            continue  # Skip the header row
                        else:
                            row = row.strip()  # Remove leading/trailing whitespaces
                            row = row.split(";")
                            # row = row.replace(
                            #     ";", " "

                            if len(row) >= 16:
                                category_id = row[14]
                                original_string = str(row[8])
                                gallery_image = str(row[13]).split(',')
                                cleaned_string = re.sub(
                                    r"[^a-zA-Z0-9 ]", "", original_string
                                )
                                category = None

                                if category_id != "":
                                    try:
                                        # Intenta obtener la categoría existente por código
                                        category = Category.objects.get(
                                            codigo=int(category_id)
                                        )
                                    except ObjectDoesNotExist:
                                        # Si la categoría no existe, crea una nueva
                                        category = Category(
                                            codigo=category_id,
                                            name=category_id,
                                            slug=category_id,
                                            image_alterna="https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Falta_imagen.jpg/640px-Falta_imagen.jpg",
                                        )
                                        category.save()

                                try:
                                    # Intenta obtener el producto existente por codigo
                                    product = Product.objects.get(
                                        codigo=row[0])

                                except ObjectDoesNotExist:
                                    product = None

                                # Si el producto no existe, crea uno nuevo
                                if product is None:
                                    product = Product(
                                        codigo=str(row[0]),
                                        name_extend=str(row[1]),
                                        description=str(
                                            row[2]) if row[2] else "",
                                        price1=int(row[3]) if row[3] else None,
                                        price2=int(row[4]) if row[4] else None,
                                        price_old=int(
                                            row[5]) if row[5] else None,
                                        flag=str(row[6]) if row[6] else "",
                                        ref=str(row[7]) if row[7] else "",
                                        slug=cleaned_string.replace(" ", "-"),
                                        active=str(row[9]) if row[9] else True,
                                        soldout=str(
                                            row[10]) if row[10] else False,
                                        offer=str(
                                            row[11]) if row[11] else False,
                                        home=str(row[12]) if row[9] else False,
                                        image_alterna=str(
                                            row[13]) if row[13] else "",
                                        qty=int(row[15]) if row[15] else None,
                                    )
                                    product.save()

                                    if any(image.strip() for image in gallery_image):
                                        for image_path in gallery_image:
                                            gallery = Gallery(
                                                product=product, image_alterna=image_path.strip())
                                            gallery.save()
                                else:
                                    # Si el producto existe, actualiza sus atributos
                                    product.name_extend = (
                                        str(row[1])
                                        if row[1] != ""
                                        else product.name_extend
                                    )
                                    product.description = (
                                        str(row[2])
                                        if row[2] != ""
                                        else product.description
                                    )
                                    product.price1 = (
                                        int(row[3]) if row[3] != "" else product.price1
                                    )
                                    product.price2 = (
                                        int(row[4]) if row[4] != "" else product.price2
                                    )
                                    product.price_old = (
                                        int(row[5])
                                        if row[5] != ""
                                        else product.price_old
                                    )
                                    product.flag = (
                                        str(row[6]) if row[6] != "" else product.flag
                                    )
                                    product.ref = (
                                        str(row[7]) if row[7] != "" else product.ref
                                    )
                                    product.slug = (
                                        cleaned_string.replace(" ", "-")
                                        if row[8] != ""
                                        else product.slug
                                    )
                                    product.active = (
                                        str(row[9]) if row[9] != "" else product.active
                                    )
                                    product.soldout = (
                                        str(row[10])
                                        if row[10] != ""
                                        else product.soldout
                                    )
                                    product.offer = (
                                        str(row[11]) if row[11] != "" else product.offer
                                    )
                                    product.home = (
                                        str(row[12]) if row[12] != "" else product.home
                                    )
                                    product.image_alterna = (
                                        str(row[13])
                                        if row[13] != ""
                                        else product.image_alterna
                                    )
                                    product.qty = (
                                        int(row[15]) if row[15] != "" else product.qty
                                    )
                                    product.save()

                                    if any(image.strip() for image in gallery_image):

                                        Gallery.objects.filter(
                                            product=product).delete()

                                        for image_path in gallery_image:
                                            gallery = Gallery(
                                                product=product, image_alterna=image_path.strip())
                                            gallery.save()

                                if category != None:
                                    try:
                                        # Intenta obtener la relacion categoría_producto existente por código
                                        category_product = CategoryProduct.objects.get(
                                            product_id=row[0]
                                        )
                                    except ObjectDoesNotExist:
                                        category_product = CategoryProduct(
                                            product_id=str(row[0]),
                                            category_id=category.id,
                                        )
                                        category_product.save()

                except Exception as e:
                    # Manejar errores generales aquí, por ejemplo, registrarlos o mostrar un mensaje de error
                    print(f"Error al procesar el archivo CSV: {str(e)}")

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_product.html", data)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("codigo", "name", "created_date")
    readonly_fields = ("created_date",)
    search_fields = ("name",)

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("upload-csv/", self.upload_csv),
        ]
        return new_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES.get("csv_upload")

            if csv_file:
                try:
                    file_data = csv_file.read().decode("utf-8")
                    csv_data = file_data.split("\n")

                    for i, row in enumerate(csv_data):
                        if i == 0:
                            continue
                        else:
                            row = row.strip()
                            row = row.split(";")

                            if len(row) >= 4:
                                original_string = str(row[2])
                                cleaned_string = re.sub(
                                    r"[^a-zA-Z0-9 ]", "", original_string
                                )

                                try:
                                    # Intenta obtener la categoría existente por Código
                                    category = Category.objects.get(
                                        codigo=row[0])
                                except ObjectDoesNotExist:
                                    category = None

                                # Si la categoría no existe, crea una nueva
                                if category is None:
                                    category = Category(
                                        codigo=row[0],
                                        name=row[1],
                                        slug=cleaned_string.replace(" ", "-"),
                                        image_alterna=row[3],
                                    )
                                    category.save()
                                else:
                                    # Si la categoría existe, actualiza sus atributos
                                    category.name = (
                                        row[1] if row[1] != "" else category.name
                                    )
                                    category.slug = (
                                        cleaned_string.replace(" ", "-")
                                        if row[2] != ""
                                        else category.slug
                                    )
                                    category.image_alterna = (
                                        row[3]
                                        if row[3] != ""
                                        else category.image_alterna
                                    )
                                    category.save()
                except Exception as e:
                    # Manejar errores generales aquí, por ejemplo, registrarlos o mostrar un mensaje de error
                    print(f"Error al procesar el archivo CSV: {str(e)}")

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_category.html", data)

class CategoryProductAdmin(admin.ModelAdmin):
    list_display = ("category", "product", "active", "created_date")
    readonly_fields = ("created_date",)
    list_display_links = ("category", "product")



admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Attribut, AttributAdmin)
# admin.site.register(Gallery, GalleryAdmin)
# admin.site.register(CategoryProduct, CategoryProductAdmin)
# admin.site.register(AttributProduct, AttributProductAdmin)
# admin.site.register(ProductEntryDetail, ProductEntryDetailAdmin)

# class AttributProductAdmin(admin.ModelAdmin):
#     list_display = ('product', 'Attribut',  'detail')


# class ProductEntryDetailAdmin(admin.ModelAdmin):
#    list_display = ('product', 'qty', 'costo', 'iva', 'ProductEntry')


# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('active', 'name_extend', 'ref', 'codigo',  'price1', 'flag', 'modified_date')
#     prepopulated_fields = {'slug': ('flag','name_extend')}
#     list_display_links = ('codigo', 'flag','name_extend')
#     search_fields = ('codigo', 'flag', 'ref', 'name_extend')
#     ordering = ('name_extend',)
#     inlines = [GalleryInline, CategoryProductInline]

# class GalleryAdmin(admin.ModelAdmin):
#     list_display = ("id", "image", "image_alterna")
#     list_display_links = ("id", "image", "image_alterna")
#     # search_fields = ('codigo', 'flag', 'ref', 'name_extend')
#     # inlines = [GalleryInline]

    # def get_urls(self):
    #     urls = super().get_urls()
    #     new_urls = [
    #         path("upload-csv/", self.upload_csv),
    #     ]
    #     return new_urls + urls

    # def upload_csv(self, request):
    #     if request.method == "POST":
    #         csv_file = request.FILES.get("csv_upload")

    #         if csv_file:
    #             try:
    #                 file_data = csv_file.read().decode("utf-8")
    #                 csv_data = file_data.split("\n")

    #                 for i, row in enumerate(csv_data):
    #                     if i == 0:
    #                         continue
    #                     else:
    #                         row = row.strip()
    #                         row = row.split(";")

    #                         if len(row) >= 3:
    #                             gallery = None
    #                             try:
    #                                 # Intenta obtener la galleria existente
    #                                 gallery = Product.objects.get(
    #                                     codigo=str(row[0]))
    #                             except ObjectDoesNotExist:
    #                                 gallery = None

    #                             if gallery is None:
    #                                 print("Producto no existe")
    #                             else:
    #                                 gallery = Gallery(
    #                                     product=gallery,
    #                                     image="",
    #                                     image_alterna=str(
    #                                         row[2]) if row[2] else "",
    #                                 )
    #                                 gallery.save()

    #             except Exception as e:
    #                 # Manejar errores generales aquí, por ejemplo, registrarlos o mostrar un mensaje de error
    #                 print(f"Error al procesar el archivo CSV: {str(e)}")

    #     form = CsvImportForm()
    #     data = {"form": form}
    #     return render(request, "admin/csv_gallery.html", data)