from django.shortcuts import render

def home(request):
    context={

    }
    return render(request,'home/app/home.html',context)