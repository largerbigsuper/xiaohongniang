"""LV URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from LV.views import UploadTokenView, ImTokenView, APPConfigView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('sms/', include('datamodels.sms.urls')),
    path('customer/', include('datamodels.role.urls')),
    path('moments/', include('datamodels.moments.urls')),
    path('notices/', include('datamodels.notices.urls')),
    path('feedback/', include('datamodels.feedback.urls')),
    path('stats/', include('datamodels.stats.urls')),
    path('token/', UploadTokenView.as_view()),
    path('im/', ImTokenView.as_view()),
    path('appconfig/', APPConfigView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
