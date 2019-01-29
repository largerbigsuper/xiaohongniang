from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProductsConfig(AppConfig):
    name = 'datamodels.products'
    verbose_name = _('产品和订单')
