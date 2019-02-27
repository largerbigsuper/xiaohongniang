from django.contrib import admin, messages
from django.utils.html import format_html

from datamodels.products.models import VirtualService, ServiceCertification, CustomerOrder, AlipayOrder, Sku, SkuExchage
from datamodels.stats.models import mm_CustomerPoint


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


@admin.register(Sku)
class SkuAdmin(admin.ModelAdmin):

    list_per_page = 20
    list_display = ('id', 'name', 'cover', 'total', 'point', 'create_at', 'in_sale')
    search_fields = ('name',)
    list_filter = ('in_sale',)
    readonly_fields = ['cover']

    def cover(self, obj):
        if obj.id:
            return format_html('<img src="%s" height="80">' % obj.cover_image.url)
        return ''

    cover.short_description = '封面图'
    cover.allow_tags = True


@admin.register(SkuExchage)
class SkuExchageAdmin(admin.ModelAdmin):

    list_per_page = 20
    list_display = ('id', 'customer', 'sku', 'create_at', 'status')
    search_fields = ('customer__account',)
    list_filter = ('status',)
    readonly_fields = ['customer', 'sku']

    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data:
            if form.initial['status'] == 0:
                if form.cleaned_data['status'] == 1:
                    # 扣除积分
                    total_point = mm_CustomerPoint.get_total_point(obj.customer.id)
                    if obj.sku.point > total_point:
                        messages.error(request, '用户积分不足')
                        return
                    mm_CustomerPoint.withdraw(obj.customer.id, request.user.id, obj.sku.point)
        super(SkuExchageAdmin, self).save_model(request, obj, form, change)
