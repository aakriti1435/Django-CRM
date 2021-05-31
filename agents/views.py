from django.shortcuts import render, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin
from django.core.mail import send_mail
import random

# Create your views here.

class AgentListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    template_name = "agents/agentList.html"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)


class CreateAgentView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "agents/createAgent.html"
    form_class  = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agentList")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"{random.randint(0, 1000000)}")
        user.save()
        Agent.objects.create(
            user = user,
            organisation = self.request.user.userprofile
        )
        send_mail(
            subject = "You are invited to be an agent.",
            message = "You are added as an agent on CRM. Please come to login and start working.",
            from_email = "aakritigupta1435@gmail.com",
            recipient_list = [user.email]
        )
        return super(CreateAgentView, self).form_valid(form)


class UpdateAgentView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/updateAgent.html"
    form_class  = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agentList")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)



class AgentDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = "agents/agentDetail.html"
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)


class AgentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agentDelete.html"
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)

    def get_success_url(self):
        return reverse("agents:agentList")

    










