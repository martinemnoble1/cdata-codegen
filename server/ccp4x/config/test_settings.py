"""
Simplified Django settings for testing async database handler.

This is a minimal configuration for running database tests without
requiring all CCP4 dependencies.
"""

import os
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "test-secret-key-not-for-production"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "ccp4x.db.config.DbConfig",  # Our database app
]

MIDDLEWARE = []

ROOT_URLCONF = None

TEMPLATES = []

# Database - Use test database from environment or in-memory
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("CCP4I2_DB_FILE", ":memory:"),
    }
}

# Internationalization
TIME_ZONE = "UTC"
USE_TZ = True

# No static files needed for testing
STATIC_URL = "/static/"

# Test projects directory
USER_DIR = Path.home().resolve() / ".ccp4x_test"
USER_DIR.mkdir(exist_ok=True)

CCP4I2_PROJECTS_DIR = USER_DIR / "test_projects"
CCP4I2_PROJECTS_DIR.mkdir(exist_ok=True)

print(f"Test Settings Loaded:")
print(f"  Database: {DATABASES['default']['NAME']}")
print(f"  Projects: {CCP4I2_PROJECTS_DIR}")
