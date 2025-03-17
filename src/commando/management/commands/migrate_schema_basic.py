from typing import Any

from django.apps import apps
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import connection
from django.core.management import BaseCommand, call_command

from helpers.db import statements as db_statements


CUSTOMER_INSTALLED_APPS = getattr(settings, 'CUSTOMER_INSTALLED_APPS', [])

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        with connection.cursor() as cursor:
            cursor.execute(db_statements.CREATE_SCHEMA_SQL.format(schema_name="public"))
            cursor.execute(db_statements.ACTIVATE_SCHEMA_SQL.format(schema_name="public"))
        # python manage.py migrate --no-input
        call_command('migrate', interactive=False)

        schemas = ["example"]
        for schema_name in schemas:
            with connection.cursor() as cursor:
                cursor.execute(db_statements.CREATE_SCHEMA_SQL.format(schema_name=schema_name))
                cursor.execute(db_statements.ACTIVATE_SCHEMA_SQL.format(schema_name=schema_name))

            for app in apps.get_app_configs():
                app_name = app.name
                if app_name not in CUSTOMER_INSTALLED_APPS:
                    continue

                try:
                    # python manage.py migrate --no-input
                    call_command('migrate', app.label, interactive=False)
                except:
                    continue


            # User = get_user_model()
            # User.objects.create_superuser(username="example", password="example1234")