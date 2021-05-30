from django.urls import path
from .views import leadList

app_name="leads"

urlpatterns = [
    path("", leadList)
]
