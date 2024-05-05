from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
       title="Vendor project API Documentation",
       default_version='v1',
       description="API description",
       terms_of_service="/",
       contact=openapi.Contact(email="manurawat771998@gmail.com"),
       license=openapi.License(name="Open source"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
from vendor_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    #vender CRUD api
    path('api/vendors/', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('api/vendors/<int:pk>/', VendorRetrieveUpdateDestroyAPIView.as_view(), name='vendor-retrieve-update-destroy'),
    
    # PO CRUD Api
    path('api/purchase_orders/', PurchaseOrderListCreateAPIView.as_view(), name='purchase-order-list-create'),
    path('api/purchase_orders/<int:pk>/', PurchaseOrderRetrieveUpdateDestroyAPIView.as_view(), name='purchase-order-retrieve-update-destroy'),
    
    #vendor performance matric
    path('api/vendors/<int:pk>/performance/', VendorPerformanceRetrieveAPIView.as_view(), name='vendor-performance'),

    path('api/purchase_orders/<int:pk>/acknowledge/', AcknowledgePurchaseOrderAPIView.as_view(), name='acknowledge-purchase-order')
]
