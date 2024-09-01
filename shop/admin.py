from django.contrib import admin
from django.db.models import Sum
from .models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'first_name', 'last_name', 'amount', 'created_at', 'total_sales', 'total_orders']
    inlines = [OrderItemInline]

    def changelist_view(self, request, extra_context=None):
        total_sales = Order.objects.aggregate(total=Sum('amount'))['total']
        total_orders = Order.objects.count()
        
        extra_context = extra_context or {}
        extra_context['total_sales'] = total_sales
        extra_context['total_orders'] = total_orders
        
        return super().changelist_view(request, extra_context=extra_context)