from django.urls import path
from .views import (
    leadListView, 
    leadDetailView, 
    createLeadView,
    updateLeadView, 
    deleteLeadView, 
    AssignAgentView,
    CategoryListView,
    CategoryDetailView, 
    UpdateCategoryView,
    FollowUpCreateView,
    FollowUpUpdateView,
    FollowUpDeleteView,
    LeadJsonView,
    LeadCategoryUpdateView,
    CategoryDeleteView,
    CategoryCreateView
)

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
    path("<int:pk>/updateCategory/", LeadCategoryUpdateView.as_view(), name='updateLeadCategory'),
    
    path('json/', LeadJsonView.as_view(), name='lead-list-json'),
    path('<int:pk>/followups/create/', FollowUpCreateView.as_view(), name='createLeadFollowup'),
    path('followups/<int:pk>/', FollowUpUpdateView.as_view(), name='lead-followup-update'),
    path('followups/<int:pk>/delete/', FollowUpDeleteView.as_view(), name='lead-followup-delete'),
    path('categories/<int:pk>/update/', UpdateCategoryView.as_view(), name='categoryUpdate'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='categoryDelete'),
    path('createCategory/', CategoryCreateView.as_view(), name='categoryCreate'),
]
