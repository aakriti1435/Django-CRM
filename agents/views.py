from django.shortcuts import render, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from .forms import AgentModelForm

# Create your views here.

class AgentListView(LoginRequiredMixin, generic.ListView):
    template_name = "agents/agentList.html"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)


class CreateAgentView(LoginRequiredMixin, generic.CreateView):
    template_name = "agents/createAgent.html"
    form_class  = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agentList")

    def form_valid(self, form):
        agent = form.save(commit=False)
        agent.organisation = self.request.user.userprofile
        agent.save()
        return super(CreateAgentView, self).form_valid(form)


class UpdateAgentView(LoginRequiredMixin, generic.UpdateView):
    template_name = "agents/updateAgent.html"
    form_class  = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agentList")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)



class AgentDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "agents/agentDetail.html"
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)


class AgentDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agentDelete.html"
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)

    def get_success_url(self):
        return reverse("agents:agentList")

    










