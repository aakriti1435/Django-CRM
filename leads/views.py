from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm
from django.views.generic import TemplateView, ListView, DetailView,CreateView, UpdateView, DeleteView
from django.core.mail import send_mail
from agents.mixins import OrganisorAndLoginRequiredMixin

# Create your views here.

class SignUpView(CreateView):
    template_name = "registration/signUp.html"
    form_class = CustomUserCreationForm
    
    def get_success_url(self):
        return reverse("login")


class HomePageView(TemplateView):
    template_name = "homePage.html"

def homePage(request):
    return render(request, "homePage.html")


class leadListView(LoginRequiredMixin, ListView):
    template_name = "leads/leadList.html"
    context_object_name = "leads" #Default name is object_list

    def get_queryset(self):
        user = self.request.user

        # Initial QuerySet of leads for entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation = user.agent.organisation)   
            # Filter leads for current agent
            queryset = queryset.filter(agent__user = user)
        return queryset


def leadList(request):
    leads = Lead.objects.all()
    context = {
        "leads" : leads
    }
    return render(request,"leads/leadList.html", context)


class leadDetailView(LoginRequiredMixin, DetailView):
    template_name = "leads/leadDetail.html"
    queryset = Lead.objects.all()
    context_object_name = "lead" #Default name is object_list

def leadDetail(request, pk):
    print(pk)
    lead = Lead.objects.get(id=pk)
    print(lead)
    context = {
        "lead" : lead
    }
    return render(request,"leads/leadDetail.html", context)


class createLeadView(OrganisorAndLoginRequiredMixin, CreateView):
    template_name = "leads/createLead.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:leadList")

    def form_valid(self, form):
        # Send Email
        send_mail(
            subject = "New Lead Created", 
            message = "Go to the site to see the new lead",
            from_email = "aakriti@gmail.com",
            recipient_list = ["aakriti1435@gmail.com"]
        )
        return super(createLeadView, self).form_valid(form)


def createLead(request):
    form = LeadModelForm()
    if(request.method == "POST"):
        print("POST Request")
        form = LeadModelForm(request.POST)
        if form.is_valid():
            # firstName = form.cleaned_data['firstName']
            # lastName = form.cleaned_data['lastName']
            # age = form.cleaned_data['age']
            # agent = form.cleaned_data['agent']
            # Lead.objects.create(
            #     firstName = firstName,
            #     lastName = lastName,
            #     age = age,
            #     agent = agent,
            # )
            form.save()
            return redirect("/leads")

    context = {
        "form": form
    }
    return render(request, "leads/createLead.html", context)


class updateLeadView(OrganisorAndLoginRequiredMixin, UpdateView):
    template_name = "leads/updateLead.html"
    form_class = LeadModelForm
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse("leads:leadList")


def updateLead(request, pk):
    lead = Lead.objects.get(id=pk)
    # form = LeadForm()
    form = LeadModelForm(instance=lead)
    if(request.method == "POST"):
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            # firstName = form.cleaned_data['firstName']
            # lastName = form.cleaned_data['lastName']
            # age = form.cleaned_data['age']
            # lead.firstName = firstName
            # lead.lastName = lastName
            # lead.age = age
            # lead.save()
            form.save()
            return redirect("/leads")

    context={ "lead":lead, "form": form }
    return render(request, "leads/updateLead.html", context)


class deleteLeadView(OrganisorAndLoginRequiredMixin, DeleteView):
    template_name = "leads/deleteLead.html"
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse("leads:leadList")

def deleteLead(request,pk):
    lead= Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")