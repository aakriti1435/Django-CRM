from django.urls import path
from .views import AgentListView, CreateAgentView, AgentDetailView, UpdateAgentView, AgentDeleteView

app_name="agents"

urlpatterns = [
    path("", AgentListView.as_view(), name='agentList'),
    path("create/", CreateAgentView.as_view(), name='createAgent'),
    path("<int:pk>/", AgentDetailView.as_view(), name='agentDetail'),
    path("<int:pk>/update/", UpdateAgentView.as_view(), name='updateAgent'),
    path("<int:pk>/delete/", AgentDeleteView.as_view(), name='deleteAgent')
]