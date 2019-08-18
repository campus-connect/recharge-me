
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, TopicSitemap, StaticAuthViewSitemap, CategorySitemap
from .views import LandingView, AboutView, ContactView, PrivacyView, TosView

sitemaps = {
    'static': StaticViewSitemap,
    'topics': TopicSitemap,
    'category': CategorySitemap,
    'auth': StaticAuthViewSitemap,
}


urlpatterns = [
    path('', LandingView.as_view(), name='landing_page'),
    path('about', AboutView.as_view(), name='about_page'),
    path('contact', ContactView.as_view(), name='contact_page'),
    path('policies', PrivacyView.as_view(), name='policies'),
    path('terms', TosView.as_view(), name='tos'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path('forum/', include('spirit.urls')),
    path('accounts/avatar/', include('avatar.urls')),
    path('accounts/notifications/',
         include('notifications.urls', namespace='notifications')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', include('robots.urls')),
    path('ads/', include('ads.urls')),
]
