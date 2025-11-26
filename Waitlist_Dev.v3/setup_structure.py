import os
import sys
from pathlib import Path

# Configuration
PROJECT_NAME = "eve_fleet_manager"
APPS = ["core", "eve_auth", "sde", "fleets", "integrations"]

def create_structure():
    base_dir = Path.cwd()
    project_root = base_dir / PROJECT_NAME
    
    print(f"🚀 Initializing project structure for '{PROJECT_NAME}'...")

    # 1. Create Root Directory
    if not project_root.exists():
        project_root.mkdir()
        print(f"   Created root directory: {project_root}")
    
    # 2. Create Manage.py placeholder (User needs to run startproject really, but this creates the folder structure)
    # Actually, let's create the folder structure manually to match a Django layout
    
    # Config dir (where settings.py lives)
    config_dir = project_root / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / "__init__.py").touch()
    (config_dir / "settings.py").touch()
    (config_dir / "urls.py").touch()
    (config_dir / "wsgi.py").touch()
    (config_dir / "asgi.py").touch()
    print("   Created configuration directory 'config'")

    # 3. Create Apps
    for app in APPS:
        app_dir = project_root / app
        app_dir.mkdir(exist_ok=True)
        (app_dir / "__init__.py").touch()
        (app_dir / "models.py").write_text("from django.db import models\n# Create your models here.\n")
        (app_dir / "views.py").write_text("from django.shortcuts import render\n# Create your views here.\n")
        (app_dir / "admin.py").write_text("from django.contrib import admin\n# Register your models here.\n")
        (app_dir / "apps.py").write_text(f"from django.apps import AppConfig\n\nclass {app.capitalize()}Config(AppConfig):\n    default_auto_field = 'django.db.models.BigAutoField'\n    name = '{app}'\n")
        
        # Create separate urls.py for each app
        (app_dir / "urls.py").write_text("from django.urls import path\nfrom . import views\n\nurlpatterns = [\n]\n")
        
        print(f"   Created app: '{app}'")

    # 4. Create Templates & Static
    templates_dir = project_root / "templates"
    static_dir = project_root / "static"
    
    templates_dir.mkdir(exist_ok=True)
    static_dir.mkdir(exist_ok=True)
    
    # Base template
    (templates_dir / "base.html").write_text("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}EVE Fleet Manager{% endblock %}</title>
    <!-- Add your CSS links here -->
</head>
<body class="bg-gray-900 text-white">
    <div id="app">
        {% block content %}{% endblock %}
    </div>
</body>
</html>""")
    
    print("   Created 'templates' and 'static' directories.")

    # 5. Create Management Command structure for SDE
    sde_mgmt_dir = project_root / "sde" / "management" / "commands"
    sde_mgmt_dir.mkdir(parents=True, exist_ok=True)
    (project_root / "sde" / "management" / "__init__.py").touch()
    (project_root / "sde" / "management" / "commands" / "__init__.py").touch()
    (sde_mgmt_dir / "update_sde.py").write_text("""from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Updates the EVE Online Static Data Export (SDE) from source'

    def handle(self, *args, **options):
        self.stdout.write('Starting SDE Update...')
        # Implementation will go here
        self.stdout.write(self.style.SUCCESS('SDE Update Complete'))
""")
    print("   Created SDE management command placeholder.")

    print(f"\n✅ Structure created! Next steps:")
    print(f"1. cd {PROJECT_NAME}")
    print(f"2. pip install -r ../requirements.txt")
    print(f"3. django-admin startproject config . (NOTE: Run this carefully to merge with existing config folder)")
    print(f"   *Alternatively, just copy the files generated here into a fresh django project*")

if __name__ == "__main__":
    create_structure()