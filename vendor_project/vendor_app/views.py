from rest_framework import generics, status
from rest_framework.response import Response
from .models import Vendor
from .serializers import *
from django.utils import timezone
from datetime import datetime

class VendorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = 'pk'

class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        vendor_id = self.request.query_params.get('vendor_id')
        if vendor_id:
            queryset = queryset.filter(vendor_id=vendor_id)
        return queryset

class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'pk'


class VendorPerformanceRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['average_response_time'] = str(data['average_response_time'] / 60) +' ' + 'min.'
        return Response(data)


class AcknowledgePurchaseOrderAPIView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.acknowledgment_date = timezone.now()
        instance.save()
        return Response(self.get_serializer(instance).data, status=status.HTTP_200_OK)