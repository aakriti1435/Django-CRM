from django.contrib import admin
from django.urls import path, include
from leads.views import homePage,HomePageView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', homePage, name='homePage'),
    path('', HomePageView.as_view(), name='homePage'),
    path("leads/",include('leads.urls', namespace="leads")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
