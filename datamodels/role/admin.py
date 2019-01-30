from datetime import datetime

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from datamodels.role.models import Customer


class VipFilter(admin.SimpleListFilter):
    title = '会员'
    parameter_name = 'vip'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('Normal', _('普通用户')),
            ('Vip', _('Vip用户')),
             )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'Normal':
            return queryset.exclude(service_vip_expired_at__lt=datetime.now())
        if self.value() == 'Vip':
            return queryset.filter(service_vip_expired_at__lt=datetime.now())


class CustomerAdmin(admin.ModelAdmin):
    # 字段为空显示内容
    # empty_value_display = '--'
    #
    # formfield_overrides = {
    #     models.TextField: {'widget': RichTextEditorWidget},
    # }

    list_display = ('account', 'name', 'age', 'gender', 'avatar_url')
    list_filter = (VipFilter, 'gender')
    # fields = ('account', 'name', 'age', 'gender', 'avatar')
    # readonly_fields = ('avatar', )

    def avatar(self, obj):
        if obj.id:
            src = 'http://lhxq.top/' + obj.avatar_url.name if obj.avatar_url else ''
            return format_html('<img src="%s" height="150">' % src)
        return ''

    avatar.short_description = '头像'
    avatar.allow_tags = True


admin.site.register(Customer, CustomerAdmin)


class Vip(Customer):

    class Meta:
        proxy = True
        verbose_name = '会员'
        verbose_name_plural = '会员'


class VipAdmin(admin.ModelAdmin):

    list_display = ('account', 'name', 'age', 'gender', 'avatar')
    list_filter = ('gender',)
    # fields = ('account', 'name', 'age', 'gender', 'avatar')
    readonly_fields = ('avatar',)

    def avatar(self, obj):
        if obj.id:
            src = 'http://lhxq.top/' + obj.avatar_url.name if obj.avatar_url else ''
            if src:
                return format_html('<img src="%s" height="80">' % src)
        return ''

    avatar.short_description = '头像'
    avatar.allow_tags = True

    def get_queryset(self, request):
        return Customer.objects.exclude(service_vip_expired_at=None)


admin.site.register(Vip, VipAdmin)

