from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm

# Create your views here.

def leadList(request):
    leads = Lead.objects.all()
    context = {
        "leads" : leads
    }
    return render(request,"leads/leadList.html", context)


def leadDetail(request, pk):
    print(pk)
    lead = Lead.objects.get(id=pk)
    print(lead)
    context = {
        "lead" : lead
    }
    return render(request,"leads/leadDetail.html", context)


def createLead(request):
    form = LeadModelForm()
    if(request.method == "POST"):
        print("POST Request")
        form = LeadModelForm(request.POST)
        if form.is_valid():
            print("Form is Valid")
            print(form.cleaned_data)
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            age = form.cleaned_data['age']
            agent = form.cleaned_data['agent']
            Lead.objects.create(
                firstName = firstName,
                lastName = lastName,
                age = age,
                agent = agent,
            )
            print("Lead created")
            return redirect("/leads")

    context = {
        "form": form
    }
    return render(request, "leads/createLead.html", context)
