from django.db import connection
from contextlib import contextmanager

from helpers.db import statements as db_statements

DEFAULT_SCHEMA = "public"


def check_if_schema_exists(schema_name: str, required_check: bool = False) -> bool:
    if schema_name == DEFAULT_SCHEMA and not required_check:
        return True

    exists = False
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT schema_name 
            FROM information_schema.schemata 
            WHERE schema_name = %s
        """, [schema_name])

        exists = cursor.fetchone() is not None
        # exists = bool(cursor.fetchone())
    return exists


def active_tenant_schema(schema_name: str) -> None:
    is_check_exists_required = schema_name != DEFAULT_SCHEMA
    schema_to_use = DEFAULT_SCHEMA
    if is_check_exists_required and check_if_schema_exists(schema_name=schema_name):
        schema_to_use = schema_name

    # if schema_to_use == connection.schema_name:
    #     print("Schema already active")
    #     return

    with connection.cursor() as cursor:
        sql = f'SET search_path TO "{schema_to_use}";'
        cursor.execute(sql)
        connection.schema_name = schema_to_use


@contextmanager
def use_public_schema(revert_schema_name=None, revert_schema=False):
    """
        with use_public_schema():
            Tenant.objects.all()
    """
    try:
        schema_to_use = DEFAULT_SCHEMA
        with connection.cursor() as cursor:
            sql = f'SET search_path TO "{schema_to_use}";'
            cursor.execute(sql)
        yield
    finally:
        if revert_schema:
            active_tenant_schema(schema_name=revert_schema_name)
