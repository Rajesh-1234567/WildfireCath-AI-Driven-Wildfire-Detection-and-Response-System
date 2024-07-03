from django.shortcuts import render
from core.models import TeamModel

def welcome(request):
    teamdetails=TeamModel.objects.all()
    context={
        'teamdetails':teamdetails,
    }
    return render(request,'core/app/welcome.html',context)