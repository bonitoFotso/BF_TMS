from django.contrib import admin
from .models import *

admin.site.register(Technicien)
admin.site.register(Tache)
admin.site.register(TechnicienTache)
admin.site.register(Rapport)
admin.site.register(Action)