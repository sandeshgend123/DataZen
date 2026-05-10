#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'datazen_website.settings')
django.setup()

from django.contrib.auth.models import User

# Update admin user to have staff privileges
admin = User.objects.get(username='admin')
admin.is_staff = True
admin.is_superuser = True
admin.save()
print("Updated admin user: is_staff=True, is_superuser=True")

print("\nAll users:")
for u in User.objects.all():
    print(f"  {u.username}: is_staff={u.is_staff}, is_superuser={u.is_superuser}")
