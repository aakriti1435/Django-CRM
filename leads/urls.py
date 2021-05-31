from django.urls import path
from .views import (leadList, leadDetail, createLead, updateLead, deleteLead, leadListView, leadDetailView, createLeadView,updateLeadView, updateLeadView, deleteLeadView, AssignAgentView,CategoryListView, CategoryDetailView, UpdateCategoryView)

app_name="leads"

urlpatterns = [
    path("", leadListView.as_view(), name='leadList'),
    path("create/", createLeadView.as_view(), name='createLead'),
    path("<int:pk>/", leadDetailView.as_view(), name='leadDetail'),
    path("<int:pk>/update/", updateLeadView.as_view(), name='updateLead'),
    path("<int:pk>/delete/", deleteLeadView.as_view(), name='deleteLead'),
    path("<int:pk>/assignAgent/", AssignAgentView.as_view(), name='assignAgent'),
    path("categories/", CategoryListView.as_view(), name="categoryList"),
    path("categoryDetail/<int:pk>/", CategoryDetailView.as_view(), name="categoryDetail"),
    path("<int:pk>/updateCategory/", UpdateCategoryView.as_view(), name='updateCategory'),
]
