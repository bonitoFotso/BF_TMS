from django.urls import  path

from .views import v

urlpatterns = [
    path('b',v,name='b')
]