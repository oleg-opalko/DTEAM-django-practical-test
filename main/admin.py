from django.contrib import admin
from .models import CV


@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'skills', 'projects', 'bio', 'contacts')


