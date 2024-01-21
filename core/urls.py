
from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static


from products.api.router import router_gallery
from products.api.router import router_product_category
from products.api.router import router_product
from products.api.router import router_productOE
from products.api.router import router_category
from warehome.api.router import router_out
from warehome.api.router import router_stock
from warehome.api.router import router_warehomedetail
from accounts.api.router import router_user
from carts.api.router import router_cart
from stores.api.router import router_order
from company.api.router import router_company
from public.api.router import route_domain

#from favorite.api.router import router_favorite
#from stores.api.router import router_categoryproduct


from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Documentation supra_enterprise_back",
        default_version='v 1.0.1',
        description="API supra_enterprise_back",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="jeffer443@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path('admin-dashboard/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),


    path('api/', include('accounts.api.router')),
    path('api/', include(route_domain.urls)),
    path('api/', include(router_category.urls)),
    path('api/', include(router_out.urls)),
    path('api/', include(router_stock.urls)),
    path('api/', include(router_user.urls)),
    path('api/', include(router_product.urls)),
    path('api/', include(router_productOE.urls)),
    path('api/', include(router_gallery.urls)),
    path('api/', include(router_product_category.urls)),
    path('api/', include(router_cart.urls)),
    path('api/', include(router_order.urls)),
    path('api/', include(router_warehomedetail.urls)),
    path('api/', include(router_company.urls)),
    #path('api/', include(router_favorite.urls)),
    # ---------------------------------------------------------------------


    #path('api/', include(router_categoryproduct.urls)),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
