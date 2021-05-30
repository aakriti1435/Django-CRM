from django.urls import path
from .views import (leadList, leadDetail, createLead, updateLead, deleteLead, leadListView, leadDetailView, createLeadView,updateLeadView, updateLeadView, deleteLeadView)

app_name="leads"

urlpatterns = [
    # path("", leadList, name='leadList'),
    path("", leadListView.as_view(), name='leadList'),
    # path("create/", createLead, name='createLead'),
    path("create/", createLeadView.as_view(), name='createLead'),
    # path("<int:pk>/", leadDetail, name='leadDetail'),
    path("<int:pk>/", leadDetailView.as_view(), name='leadDetail'),
    # path("<int:pk>/update/", updateLead, name='updateLead'),
    path("<int:pk>/update/", updateLeadView.as_view(), name='updateLead'),
    # path("<int:pk>/delete/", deleteLead, name='deleteLead'),
    path("<int:pk>/delete/", deleteLeadView.as_view(), name='deleteLead')
]
