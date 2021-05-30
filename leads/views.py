from django.shortcuts import render
from django.http import HttpResponse
from .models import Lead

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