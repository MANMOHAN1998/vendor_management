from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *
from django.utils import timezone


@receiver(post_save, sender=PurchaseOrder)
def calculate_average_response_time(sender, instance, created, **kwargs):
    if created:
        return
    vendor = instance.vendor
    response_time = (instance.acknowledgment_date - instance.issue_date).total_seconds()
    vendor_purchase_orders = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
    total_purchase_orders = vendor_purchase_orders.count()
    total_response_time = sum(abs((po.acknowledgment_date - po.issue_date).total_seconds()) for po in vendor_purchase_orders)
    average_response_time = total_response_time / total_purchase_orders if total_purchase_orders else 0
    vendor.average_response_time = average_response_time
    vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_on_time_delivery_rate(sender, instance, created, **kwargs):
    if not created and instance.status == 'completed':
        vendor = instance.vendor
        total_completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
        on_time_delivered_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed', delivery_date__gte=timezone.now()).count()
        on_time_delivery_rate = on_time_delivered_orders / total_completed_orders if total_completed_orders else 0
        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_quality_rating_avg(sender, instance, created, **kwargs):
    if not created and instance.quality_rating is not None:
        vendor = instance.vendor
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, quality_rating__isnull=False)
        quality_rating_avg = completed_orders.aggregate(avg_quality_rating=models.Avg('quality_rating'))['avg_quality_rating']
        vendor.quality_rating_avg = quality_rating_avg or 0
        vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_fulfillment_rate(sender, instance, **kwargs):
    vendor = instance.vendor
    total_orders = PurchaseOrder.objects.filter(vendor=vendor).count()
    fulfilled_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
    fulfillment_rate = (fulfilled_orders / total_orders) * 100 if total_orders else 0
    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()
