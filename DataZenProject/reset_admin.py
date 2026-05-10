#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'datazen_website.settings')
django.setup()

from django.contrib.auth.models import User

# Reset admin password
u = User.objects.get(username='admin')
u.set_password('admin123')
u.save()
print(f"Reset password for {u.username}")
