from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def homePage(request):
    # return HttpResponse("Home Page")
    return render(request,"leads/homePage.html")