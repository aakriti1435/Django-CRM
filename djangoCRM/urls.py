from django.contrib import admin
from django.urls import path, include
from leads.views import homePage, HomePageView, SignUpView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', homePage, name='homePage'),
    path('', HomePageView.as_view(), name='homePage'),
    path("leads/",include('leads.urls', namespace="leads")),
    path("agents/",include('agents.urls', namespace="agents")),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
