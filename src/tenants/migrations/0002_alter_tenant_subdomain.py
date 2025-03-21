# Generated by Django 5.0.13 on 2025-03-18 18:02

import helpers.db.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='subdomain',
            field=models.CharField(db_index=True, max_length=60, unique=True, validators=[helpers.db.validators.validate_blocked_subdomains, helpers.db.validators.validate_subdomain]),
        ),
    ]
