import os
import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hydroponicsystem.settings") 

django.setup()
