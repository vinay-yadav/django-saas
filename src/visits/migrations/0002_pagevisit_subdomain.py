# Generated by Django 5.0.13 on 2025-03-17 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagevisit',
            name='subdomain',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
