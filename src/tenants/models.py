import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.management import call_command

from . import utils, tasks
from helpers.db.validators import (validate_blocked_subdomains, validate_subdomain)

User = settings.AUTH_USER_MODEL

class Tenant(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, db_index=True, editable=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    subdomain = models.CharField(
        max_length=60, unique=True, db_index=True, validators=[validate_blocked_subdomains, validate_subdomain]
    )
    schema_name = models.CharField(max_length=60, unique=True, blank=True, null=True, db_index=True)
    active = models.BooleanField(default=True)
    active_at = models.DateTimeField(null=True, blank=True)
    inactive_at = models.DateTimeField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subdomain}:{self.id}"

    def save(self, *args, **kwargs):
        now = timezone.now()
        if self.active and not self.active_at:
            self.active_at = now
            self.inactive_at = None
        elif not self.active and not self.inactive_at:
            self.active_at = None
            self.inactive_at = now

        if not self.schema_name:
            self.schema_name = utils.generate_unique_schema_name(self.id)

        super(Tenant, self).save(*args, **kwargs)
        tasks.migrate_tenant_task(self.id)
