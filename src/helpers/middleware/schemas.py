from django.db import connection
from django.apps import apps
from django.core.cache import cache
from django.http import HttpResponse

from helpers.db.schemas import (
    use_public_schema, active_tenant_schema
)
from helpers.db import statements as db_statements


class SchemaTenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        host = request.get_host()
        host_portless = host.split(':')[0]
        host_split = host_portless.split('.')

        subdomain = None
        if len(host_split) > 1:
            subdomain = host_split[0]

        print('host', host, host_portless, host_split, subdomain)

        schema_name, tenant_active = self.get_schema_name(subdomain=subdomain)
        active_tenant_schema(schema_name=schema_name)

        request.tenant_active = tenant_active

        if not tenant_active:
            return HttpResponse("Invalid subdomain")
        return self.get_response(request)

    def get_schema_name(self, subdomain=None):
        if subdomain in [None, "localhost", "desalsa"]:
            return "public", True

        schema_name = "public"
        cache_subdomain_key = f"subdomain_schema:{subdomain}"
        cache_subdomain_value = cache.get(cache_subdomain_key)

        cache_subdomain_valid_key = f"subdomain_valid_schema:{subdomain}"
        cache_subdomain_valid_value = cache.get(cache_subdomain_valid_key)

        if cache_subdomain_value and cache_subdomain_valid_value:
            print("Schema cache hit", cache_subdomain_value)
            return cache_subdomain_value, cache_subdomain_valid_value

        tenant_active = False
        with use_public_schema():
            Tenant = apps.get_model("tenants", "Tenant")
            try:
                obj = Tenant.objects.get(subdomain=subdomain)
                schema_name = obj.schema_name
                tenant_active = True
            except Tenant.DoesNotExist:
                print(f"{subdomain} does not exist as Tenant")
            except Exception as e:
                print(f"{subdomain} does not exist as Tenant. \n {e}")

            cache_ttl = 60 # seconds
            cache.set(cache_subdomain_key, str(schema_name), cache_ttl)
            cache.set(cache_subdomain_valid_key, tenant_active, cache_ttl)
        return schema_name, tenant_active
