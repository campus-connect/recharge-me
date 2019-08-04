"""recharge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap
from .views import LandingView, AboutView, ContactView

sitemaps = {
    'static': StaticViewSitemap,
}


urlpatterns = [
    path('', LandingView.as_view(), name='landing_page'),
    path('about', AboutView.as_view(), name='about_page'),
    path('contact', ContactView.as_view(), name='contact_page'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/avatar/', include('avatar.urls')),
    path('accounts/notifications/', include('notifications.urls', namespace='notifications')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt',include('robots.urls')),
]
