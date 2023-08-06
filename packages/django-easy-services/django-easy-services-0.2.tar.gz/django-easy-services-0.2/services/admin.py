from django.contrib import admin
from .models import *


class ServiceFailoverInline(admin.TabularInline):
    model = ServiceFailover
    extra = 0
    sortable_field_name = 'order'
    fk_name = 'service'


class ServiceAdmin(admin.ModelAdmin):
    inlines = [ServiceFailoverInline]


admin.site.register(Service, ServiceAdmin)

