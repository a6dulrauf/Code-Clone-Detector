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

        # (project name, language, [(slot, source path)])
        demos = [
            ("demo-comparison", "java", [
                ("project1", os.path.join(samples, "Original.java")),
                ("project2", os.path.join(samples, "NearClone.java")),
            ]),
            ("demo-comparison-python", "python", [
                ("project1", os.path.join(samples, "demo-projects-python", "project-a", "calculator.py")),
                ("project2", os.path.join(samples, "demo-projects-python", "project-b", "math_helper.py")),
            ]),
            ("demo-comparison-js", "javascript", [
                ("project1", os.path.join(samples, "demo-projects-js", "project-a", "calculator.js")),
                ("project2", os.path.join(samples, "demo-projects-js", "project-b", "mathHelper.js")),
            ]),
        ]
        for name, language, files in demos:
            proj = os.path.join(settings.BASE_DIR, "projects", DEMO_USER, name)
            for sub, src in files:
                dest = os.path.join(proj, sub)
                os.makedirs(dest, exist_ok=True)
                if os.path.exists(src):
                    shutil.copy(src, os.path.join(dest, os.path.basename(src)))
            with open(os.path.join(proj, ".ccd_language"), "w") as marker:
                marker.write(language)
            self.stdout.write("demo project seeded: projects/%s/%s (%s)" % (DEMO_USER, name, language))
