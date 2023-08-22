from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, UpdateView,DetailView,View,ListView,TemplateView
from apps.project.models import *
from apps.clients.models import *

# Create your views here.
class DashView(TemplateView):
    template_name = "h.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tache"] = Tache
        context["appelants"] = Appelant.objects.all()
        return context
    


def v1(request):
    return render(request,'h.html')