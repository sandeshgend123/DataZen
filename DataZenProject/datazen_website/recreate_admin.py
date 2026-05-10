#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'datazen_website.settings')
django.setup()

from django.contrib.auth.models import User

# Delete existing admin user if it exists
User.objects.filter(username='admin').delete()

# Create new admin user
admin = User.objects.create_user(username='admin', email='admin@test.com', password='admin123')
admin.is_staff = True
admin.is_superuser = True
admin.save()

print(f"Created admin user: {admin.username}, is_staff={admin.is_staff}")

# Verify it works with authenticate
from django.contrib.auth import authenticate
test_user = authenticate(username='admin', password='admin123')
print(f"Authenticate result: {test_user}")

if test_user:
    print(f"Authentication successful! is_staff={test_user.is_staff}")
else:
    print("Authentication failed!")

print("\nAll users:")
for u in User.objects.all():
    print(f"  {u.username}: is_staff={u.is_staff}")
