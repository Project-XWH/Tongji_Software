from django.contrib import admin
# account
from .models import Advice
admin.site.register(Advice)
class AdviceAdmin(admin.ModelAdmin):
    list_display = ('text', 'advice_time', 'user')

