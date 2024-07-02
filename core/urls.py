from core import views
from django.urls import path

app_name="core"

urlpatterns=[
    path("",views.welcome,name="welcome"),
]
