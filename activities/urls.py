from django.urls import path
from . import views

urlpatterns = [
    path('activitieslist/',views.activitieslist,name='activities_list'),
]