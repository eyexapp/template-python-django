"""Celery tasks for the users app."""

from __future__ import annotations

import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(name="users.send_welcome_email")
def send_welcome_email(user_id: int) -> None:
    """Send a welcome email to a newly registered user.

    This is an example Celery task demonstrating the async task pattern.
    Replace with actual email sending logic.
    """
    from django.contrib.auth import get_user_model

    user_model = get_user_model()
    try:
        user = user_model.objects.get(pk=user_id)
        logger.info("Sending welcome email to %s", user.email)
        # TODO: Implement actual email sending
        # send_mail("Welcome!", "...", "noreply@example.com", [user.email])
    except user_model.DoesNotExist:
        logger.warning("User %s not found — skipping welcome email", user_id)
