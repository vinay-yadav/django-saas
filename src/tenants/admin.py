from django.contrib import admin

from .models import Tenant


class TenantAdmin(admin.ModelAdmin):
    readonly_fields = ('schema_name', 'timestamp', 'updated', 'active_at', 'inactive_at')
    list_display = ("subdomain", "owner", "schema_name")

admin.site.register(Tenant, TenantAdmin)
