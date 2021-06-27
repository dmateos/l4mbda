from django.contrib import admin
from .models import Job


def run_job(modeladmin, request, queryset):
    for n in queryset:
        n.run()


class JobAdmin(admin.ModelAdmin):
    actions = [run_job]


admin.site.register(Job, JobAdmin)
