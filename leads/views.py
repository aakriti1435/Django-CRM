from django.shortcuts import render
from django.http import HttpResponse
from .models import Lead

# Create your views here.

def leadList(request):
    # return HttpResponse("Home Page")
    # context = {"name":"Aakriti"}
    leads = Lead.objects.all()
    context = {
        "leads" : leads
    }
    return render(request,"leads/leadList.html", context)