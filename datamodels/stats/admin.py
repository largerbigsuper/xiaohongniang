from django.contrib import admin, messages

from datamodels.stats.models import CustomerBonusRecord, WithDrawRecord, mm_CustomerBonusRecord


@admin.register(CustomerBonusRecord)
class CustomerBonusRecordAdmin(admin.ModelAdmin):

    list_per_page = 20
    list_display = ('id', 'customer', 'from_customer', 'in_or_out', 'amount',
                    'total_left', 'desc', 'operator', 'create_at')
    search_fields = ('customer__acount',)


@admin.register(WithDrawRecord)
class WithDrawRecordAdmin(admin.ModelAdmin):

    list_per_page = 20
    list_display = ('customer', 'status', 'amount', 'operator')
    list_filter = ('status',)
    search_fields = ('customer__acount',)

    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data:
            if form.initial['status'] == 0:
                if form.cleaned_data['status'] == 1:
                    # 扣除余额
                    total_point = mm_CustomerBonusRecord.get_total_point(obj.customer.id)
                    if obj.amount > total_point:
                        messages.error(request, '用户积分不足')
                        return
                    else:
                        mm_CustomerBonusRecord.add_record(
                            customer_id=obj.customer.id,
                            from_customer_id=obj.customer.id,
                            action=mm_CustomerBonusRecord.Action_Withdraw,
                            amount=obj.amount,
                            desc=mm_CustomerBonusRecord.template_withdraw,
                            operator_id=request.user.id
                        )

        super(WithDrawRecordAdmin, self).save_model(request, obj, form, change)