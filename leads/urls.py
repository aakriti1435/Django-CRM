from django.urls import path
from .views import leadList,leadDetail,createLead

app_name="leads"

urlpatterns = [
    path("", leadList),
    path("create/", createLead),
    path("<int:pk>/", leadDetail)
]
