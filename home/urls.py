from home import views
from django.urls import path

app_name="home"

urlpatterns=[
    path("",views.home,name="home"),
    path("loading...",views.loading,name="loading"),
    path("map",views.mapview,name="map"),
]
