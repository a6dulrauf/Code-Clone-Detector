from django.apps import AppConfig


class CodecloneConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CodeClone'

    def ready(self):
        # Register any user-uploaded language definitions into the engine
        # registry so they're available for comparisons this run. Guarded so a
        # not-yet-migrated DB (e.g. during `migrate`) doesn't break startup.
        from com.vsa.elements import languages
        try:
            from .models import LanguageDefinition
            for row in LanguageDefinition.objects.all():
                try:
                    languages.register_definition(row.payload)
                except Exception:
                    pass
        except Exception:
            pass
