from django.contrib import admin
from django.urls import path, include
from leads.views import homePage,HomePageView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', homePage, name='homePage'),
    path('', HomePageView.as_view(), name='homePage'),
    path("leads/",include('leads.urls', namespace="leads")),

]
