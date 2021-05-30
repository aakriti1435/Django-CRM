from django.urls import path
from .views import leadList,leadDetail,createLead,updateLead,deleteLead

app_name="leads"

urlpatterns = [
    path("", leadList),
    path("create/", createLead),
    path("<int:pk>/", leadDetail),
    path("<int:pk>/update/", updateLead),
    path("<int:pk>/delete/", deleteLead)
]
