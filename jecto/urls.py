"""jecto URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import profiles.urls
import accounts.urls
from . import views
from .api import InjectionSiteResource, InjectionResource


# Personalized admin site settings like title and header
admin.site.site_title = 'Jecto Site Admin'
admin.site.site_header = 'Jecto Administration'


urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('about/', views.AboutPage.as_view(), name='about'),
    path('users/', include(profiles.urls)),
    path('admin/', admin.site.urls),
    path('api/sites/', include(InjectionSiteResource.urls())),
    path('api/injections/', include(InjectionResource.urls())),
    path('', include(accounts.urls)),


]

# User-uploaded files like profile pics need to be served in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Include django debug toolbar if DEBUG is on
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
