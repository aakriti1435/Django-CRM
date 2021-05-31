from django.urls import path
from .views import AgentListView, CreateAgentView, AgentDetailView

app_name="agents"

urlpatterns = [
    path("", AgentListView.as_view(), name='agentList'),
    path("create/", CreateAgentView.as_view(), name='createAgent'),
    path("<int:pk>/", AgentDetailView.as_view(), name='agentDetail'),
    # path("<int:pk>/update/", updateLeadView.as_view(), name='updateLead'),
    # path("<int:pk>/delete/", deleteLeadView.as_view(), name='deleteLead')
]