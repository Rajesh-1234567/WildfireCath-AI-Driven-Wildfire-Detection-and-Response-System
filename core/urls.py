from core import views
from django.urls import path

app_name="core"

urlpatterns=[
    path("",views.welcome,name="welcome"),
    path('send-message/', views.send_message, name='send_message'),
]
