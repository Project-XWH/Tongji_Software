from django.contrib import admin
# Register your models here.
# path_search

from .models import CompoundsName
import pickle
admin.site.register(CompoundsName)
