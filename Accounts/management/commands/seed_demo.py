import os
import shutil

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

DEMO_USER = "demo"
DEMO_PASS = "demo12345"


class Command(BaseCommand):
    help = "Create the demo user and a seeded demo project."

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username=DEMO_USER, defaults={"email": "demo@example.com"})
        user.set_password(DEMO_PASS)
        user.is_active = True
        user.save()
        self.stdout.write(f"demo user {'created' if created else 'updated'}: {DEMO_USER}/{DEMO_PASS}")

        samples = os.path.join(settings.BASE_DIR, "samples")
        for proj, files in (("project1", ["Original.java"]), ("project2", ["NearClone.java"])):
            dest = os.path.join(settings.BASE_DIR, "projects", DEMO_USER, proj)
            os.makedirs(dest, exist_ok=True)
            for f in files:
                src = os.path.join(samples, f)
                if os.path.exists(src):
                    shutil.copy(src, os.path.join(dest, f))
        self.stdout.write("demo project seeded under projects/demo/")
