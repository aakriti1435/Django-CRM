from django.contrib import admin
from django.urls import path, include
from leads.views import homePage, HomePageView, SignUpView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', homePage, name='homePage'),
    path('', HomePageView.as_view(), name='homePage'),
    path("leads/",include('leads.urls', namespace="leads")),
    path("agents/",include('agents.urls', namespace="agents")),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("resetPassword/", PasswordResetView.as_view(), name="resetPassword"),
    path("resetPasswordDone/", PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("resetPasswordConfirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("resetPasswordComplete/", PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
