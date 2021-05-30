from django.urls import path
from .views import leadList,leadDetail,createLead,updateLead,deleteLead

app_name="leads"

urlpatterns = [
    path("", leadList, name='leadList'),
    path("create/", createLead, name='createLead'),
    path("<int:pk>/", leadDetail, name='leadDetail'),
    path("<int:pk>/update/", updateLead, name='updateLead'),
    path("<int:pk>/delete/", deleteLead, name='deleteLead')
]
