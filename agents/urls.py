from django.urls import path
from .views import AgentListView, CreateAgentView

app_name="agents"

urlpatterns = [
    path("", AgentListView.as_view(), name='agentList'),
    path("create/", CreateAgentView.as_view(), name='createAgent'),
]