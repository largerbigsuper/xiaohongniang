from django.contrib import admin

from datamodels.products.models import VirtualService, ServiceCertification, CustomerOrder, AlipayOrder


@admin.register(VirtualService)
class VirtualServiceAdmin(admin.ModelAdmin):

    list_per_page = 20
    list_display = ('id', 'service_type', 'name', 'pricelist_admin', 'detail', 'create_at')
    exclude = ('create_at',)
    list_filter = ('service_type', 'create_at')
    search_fields = ('name',)
    readonly_fields = ('pricelist_admin', )


@admin.register(ServiceCertification)
class ServiceCertificationAdmin(admin.ModelAdmin):

    list_per_page = 20
    list_display = ('id', 'customer', 'virtual_service', 'expired_at')
    fields = ('customer', 'virtual_service', 'expired_at')
    list_filter = ('virtual_service', 'expired_at')
    search_fields = ('customer__account',)


@admin.register(CustomerOrder)
class CustomerOrderAdmin(admin.ModelAdmin):

    list_per_page = 20
    list_display = ('id', 'customer', 'pay_type', 'union_trade_no', 'service_name', 'total_amount', 'create_at',
                    'content_object')
    fields = ('customer', 'pay_type', 'union_trade_no', 'service_name', 'total_amount', 'content_type', 'object_id')
    list_filter = ('pay_type', 'create_at')
    search_fields = ('customer__account',)


@admin.register(AlipayOrder)
class AlipayOrderAdmin(admin.ModelAdmin):

    list_per_page = 20
    list_display = ('id', 'customer', 'status', 'virtual_service', 'union_trade_no',
                    'trade_no', 'total_amount', 'create_at')
    exclude = ('create_at',)
    list_filter = ('status', 'create_at')
    search_fields = ('customer__account', 'union_trade_no')
