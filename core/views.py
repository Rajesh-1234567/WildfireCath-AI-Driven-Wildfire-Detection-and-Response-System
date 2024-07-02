from django.shortcuts import render

def welcome(request):
    context={

    }
    return render(request,'core/app/welcome.html',context)