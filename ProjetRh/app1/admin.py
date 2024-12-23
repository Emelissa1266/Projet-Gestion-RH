from django.contrib import admin
from .models import Employe
from .models import Evaluation
from .models import Conge
from .models import Contrat
from .models import Salaire
from .models import Service

# Register your models here.
admin.site.register(Employe)
admin.site.register(Evaluation)
admin.site.register(Conge)
admin.site.register(Contrat)
admin.site.register(Salaire)
admin.site.register(Service)

