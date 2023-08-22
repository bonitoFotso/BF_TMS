
from django.urls import  path

from .views import *

urlpatterns = [
    path('b1',DashView.as_view(),name='dashboard')
]