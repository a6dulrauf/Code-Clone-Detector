from django.db import models


class LanguageDefinition(models.Model):
    """A user-uploaded language definition, registered into the engine at
    startup and on upload. On a no-persistent-disk host (e.g. Render free tier)
    these reset when the instance restarts — the same as uploaded projects."""

    name = models.CharField(max_length=40, unique=True)
    label = models.CharField(max_length=60, blank=True)
    payload = models.JSONField()          # the full definition dict
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
