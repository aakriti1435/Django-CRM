import datetime
import logging
from django import contrib
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.http.response import JsonResponse
from .models import Lead, Agent, Category, FollowUp
from .forms import (LeadForm, LeadModelForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm, CategoryModelForm, FollowUpModelForm)
from django.views.generic import (TemplateView, ListView, DetailView,CreateView, UpdateView, DeleteView, FormView, View)
from django.core.mail import send_mail
from agents.mixins import OrganisorAndLoginRequiredMixin

# Create your views here.

logger = logging.getLogger(__name__)


class SignUpView(CreateView):
    template_name = "registration/signUp.html"
    form_class = CustomUserCreationForm
    
    def get_success_url(self):
        return reverse("login")


class HomePageView(TemplateView):
    template_name = "homePage.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)


def homePage(request):
    return render(request, "homePage.html")


class leadListView(LoginRequiredMixin, ListView):
    template_name = "leads/leadList.html"
    context_object_name = "leads" #Default name is object_list

    def get_queryset(self):
        user = self.request.user

        # Initial QuerySet of leads for entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organisation = user.agent.organisation, agent__isnull=False)   
            # Filter leads for current agent
            queryset = queryset.filter(agent__user = user)
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(leadListView, self).get_context_data(**kwargs)
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.userprofile, agent__isnull=True)
            context.update({
                "unassignedLeads": queryset
            })
        return context


def leadList(request):
    leads = Lead.objects.all()
    context = {
        "leads" : leads
    }
    return render(request,"leads/leadList.html", context)


class leadDetailView(LoginRequiredMixin, DetailView):
    template_name = "leads/leadDetail.html"
    context_object_name = "lead" #Default name is object_list

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
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        messages.success(self.request, "You have successfully created a lead")
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

    def get_success_url(self):
        return reverse("leads:leadList")

    def get_queryset(self):
        user = self.request.user
        # Initial QuerySet of leads for entire organisation
        return Lead.objects.filter(organisation = user.userprofile)

    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(updateLeadView, self).form_valid(form)


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
    
    def get_queryset(self):
        user = self.request.user
        # Initial QuerySet of leads for entire organisation
        return Lead.objects.filter(organisation = user.userprofile)

    def get_success_url(self):
        return reverse("leads:leadList")


def deleteLead(request,pk):
    lead= Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")


class AssignAgentView(OrganisorAndLoginRequiredMixin, FormView):
    template_name = "leads/assignAgent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:leadList")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id = self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "leads/categoryList.html"
    context_object_name = "categoryList"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        # Initial QuerySet of leads for entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation = user.agent.organisation)   
        context.update({
            "unassignedLeadCount": queryset.filter(category__isnull = True).count()
        })
        return context
    
    def get_queryset(self):
        user = self.request.user
        # Initial QuerySet of leads for entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(organisation = user.userprofile)
        else:
            queryset = Category.objects.filter(organisation = user.agent.organisation)   
        return queryset


class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "leads/categoryDetail.html"
    context_object_name = "category"

    # def get_context_data(self, **kwargs):
    #     context = super(CategoryDetailView, self).get_context_data(**kwargs)
    #     queryset = Lead.objects.filter(category = self.get_object())
    #     queryset = self.get_object().lead_set.all()
    #     leads = self.get_object().leads.all()
    #     context.update({
    #         "leads" : leads
    #     })
    #     return context    

    def get_queryset(self):
        user = self.request.user
        # Initial QuerySet of leads for entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(organisation = user.userprofile)
        else:
            queryset = Category.objects.filter(organisation = user.agent.organisation)   
        return queryset


class CategoryCreateView(OrganisorAndLoginRequiredMixin, CreateView):
    template_name = "leads/createCategory.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:categoryList")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organisation = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView, self).form_valid(form)


class UpdateCategoryView(OrganisorAndLoginRequiredMixin, UpdateView):
    template_name = "leads/updateCategory.html"
    form_class = LeadCategoryUpdateForm

    def get_success_url(self):
        return reverse("leads:categoryList")

    def get_queryset(self):
        user = self.request.user

        # Initial QuerySet of leads for entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation = user.agent.organisation)   
        return queryset


class DashboardView(OrganisorAndLoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        user = self.request.user

        # How many leads we have in total
        total_lead_count = Lead.objects.filter(organisation=user.userprofile).count()

        # How many new leads in the last 30 days
        thirty_days_ago = datetime.date.today() - datetime.timedelta(days=30)

        total_in_past30 = Lead.objects.filter(
            organisation=user.userprofile,
            dateAdded__gte=thirty_days_ago
        ).count()

        # How many converted leads in the last 30 days
        converted_category = Category.objects.get(name="Converted")
        converted_in_past30 = Lead.objects.filter(
            organisation=user.userprofile,
            category=converted_category,
            converted_date__gte=thirty_days_ago
        ).count()

        context.update({
            "total_lead_count": total_lead_count,
            "total_in_past30": total_in_past30,
            "converted_in_past30": converted_in_past30
        })
        return context


class CategoryDeleteView(OrganisorAndLoginRequiredMixin, DeleteView):
    template_name = "leads/deleteCategory.html"

    def get_success_url(self):
        return reverse("leads:categoryList")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "leads/leadCategoryUpdate.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:leadDetail", kwargs={"pk": self.get_object().id})

    def form_valid(self, form):
        lead_before_update = self.get_object()
        instance = form.save(commit=False)
        converted_category = Category.objects.get(name="Converted")
        if form.cleaned_data["category"] == converted_category:
            # update the date at which this lead was converted
            if lead_before_update.category != converted_category:
                # this lead has now been converted
                instance.converted_date = datetime.datetime.now()
        instance.save()
        return super(LeadCategoryUpdateView, self).form_valid(form)


class FollowUpCreateView(LoginRequiredMixin,CreateView):
    template_name = "leads/followup_create.html"
    form_class = FollowUpModelForm

    def get_success_url(self):
        return reverse("leads:leadDetail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super(FollowUpCreateView, self).get_context_data(**kwargs)
        context.update({
            "lead": Lead.objects.get(pk=self.kwargs["pk"])
        })
        return context

    def form_valid(self, form):
        lead = Lead.objects.get(pk=self.kwargs["pk"])
        followup = form.save(commit=False)
        followup.lead = lead
        followup.save()
        return super(FollowUpCreateView, self).form_valid(form)


class FollowUpUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "leads/followup_update.html"
    form_class = FollowUpModelForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = FollowUp.objects.filter(lead__organisation=user.userprofile)
        else:
            queryset = FollowUp.objects.filter(lead__organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(lead__agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:leadDetail", kwargs={"pk": self.get_object().lead.id})


class FollowUpDeleteView(OrganisorAndLoginRequiredMixin, DeleteView):
    template_name = "leads/followup_delete.html"

    def get_success_url(self):
        followup = FollowUp.objects.get(id=self.kwargs["pk"])
        return reverse("leads:leadDetail", kwargs={"pk": followup.lead.pk})

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = FollowUp.objects.filter(lead__organisation=user.userprofile)
        else:
            queryset = FollowUp.objects.filter(lead__organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(lead__agent__user=user)
        return queryset


class LeadJsonView(View):

    def get(self, request, *args, **kwargs):
        
        qs = list(Lead.objects.all().values(
            "first_name", 
            "last_name", 
            "age")
        )

        return JsonResponse({
            "qs": qs,
        })





