"""
URL configuration for registry_office project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.common.urls')),
    path('auth/', include('apps.accounts.urls')),
    path('profile/', include('apps.user_profiles.urls')),
    path('incoming/', include('apps.incoming_log.urls')),
    path('outgoing/', include('apps.outgoing_log.urls')),
    path('orders/', include('apps.administrative_orders_log.urls')),
    path('contracts/', include('apps.contracts_log.urls')),
    path('newsletter/', include('apps.news_feed.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
