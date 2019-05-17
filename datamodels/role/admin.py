import json
from datetime import datetime

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from datamodels.role.models import Customer, Picture, mm_Picture
from lib.im import IMServe


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
            return queryset.filter(service_vip_expired_at__gt=datetime.now())


class CustomerAdmin(admin.ModelAdmin):

    list_per_page = 20

    def get_queryset(self, request):
        return super(CustomerAdmin, self).get_queryset(request).select_related('user')

    list_display = ('account', 'name', 'age', 'gender', 'date_joined')
    list_filter = (VipFilter, 'gender', 'user__date_joined')
    # fields = ('account', 'name', 'age', 'gender', 'avatar')
    readonly_fields = ('avatar', 'images_list')
    search_fields = ('account', 'name')

    def avatar(self, obj):
        if obj.id:
            return format_html('<img src="%s" height="80">' % obj.avatar_url)
        return ''

    avatar.short_description = '头像'
    avatar.allow_tags = True

    def images_list(self, obj):
        json_list = json.loads(obj.images)
        images = ''
        for url in json_list:
            images += '<img src="%s"  style = "height:178px; width:130px;margin-right:20px" >' % url
        html = '<div>' + images + '</div>'
        return format_html(html)

    images_list.short_description = '相册'
    images_list.allow_tags = True

    def date_joined(self, obj):
        return obj.user.date_joined
    date_joined.short_description = '注册时间'
    date_joined.allow_tags = True


admin.site.register(Customer, CustomerAdmin)


def make_verified(modeladmin, request, queryset):
    for picture in queryset:
        picture.customer.avatar_url = picture.url
        picture.customer.avatar_status = 1
        picture.customer.save()
        picture.is_verified = True
        picture.save()
        IMServe.refresh_token(picture.customer.id, picture.customer.name, picture.url)


make_verified.short_description = "通过验证"


def make_failed(modeladmin, request, queryset):
    for picture in queryset:
        # picture.customer.avatar_url = picture.url
        if picture.customer.avatar_url:
            picture.customer.avatar_status = 1
        else:
            picture.customer.avatar_status = 0
        picture.customer.save()


make_failed.short_description = "未通过验证"


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('id', 'avatar')
    readonly_fields = ('avatar', )
    actions = [make_verified, make_failed]

    def get_queryset(self, request):
        return mm_Picture.filter(is_verified=False)

    def avatar(self, obj):
        if obj.url:
            return format_html('<img src="%s" height="80">' % obj.url)
        return ''

    avatar.short_description = '头像'
    avatar.allow_tags = True


