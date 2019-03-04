from django.contrib import admin

from datamodels.notices.models import Notice, Demand, mm_Demand
from datamodels.products.models import mm_VirtualService


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):

    list_per_page = 20
    list_display = ('id', 'action_type', 'content_type', 'object_id',
                    'content_type_result', 'result_id',
                    'from_customer', 'to_customer', 'status')


@admin.register(Demand)
class Demand(admin.ModelAdmin):

    list_per_page = 20
    list_display = ('id', 'demand_type', 'customer', 'to_customer', 'status', 'create_at')
    list_filter = ('demand_type', 'status', 'create_at')

    def save_model(self, request, obj, form, change):
        # 返回用户的服务卡
        if 'status' in form.changed_data:
            if form.initial['status'] == 0:
                if form.cleaned_data['status'] == mm_Demand.Status_Refused:
                    service_type = mm_VirtualService.Demand_Type_2_Service_Type.get(obj.demand_type, 0)
                    mm_VirtualService.modify_card(obj.customer_id, service_type, 1)
        super().save_model(request, obj, form, change)

