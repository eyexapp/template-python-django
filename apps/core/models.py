"""Abstract base models for all apps."""

from __future__ import annotations

import uuid

from django.db import models


class TimeStampedModel(models.Model):
    """Abstract model with automatic created_at / updated_at fields."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """Abstract model with UUID primary key."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class BaseModel(TimeStampedModel, UUIDModel):
    """Abstract model combining UUID primary key and timestamps.

    Use this as the base for most domain models::

        class Product(BaseModel):
            name = models.CharField(max_length=255)
    """

    class Meta:
        abstract = True
        ordering = ["-created_at"]
