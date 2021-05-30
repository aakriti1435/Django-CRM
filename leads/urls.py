from django.urls import path
from .views import leadList,leadDetail

app_name="leads"

urlpatterns = [
    path("", leadList),
    path("<pk>/", leadDetail)
]
