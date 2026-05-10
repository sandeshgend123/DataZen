#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'datazen_website.settings')
django.setup()

from django.contrib.auth.models import User

# Create or update user1
user1, created = User.objects.get_or_create(username='user1', defaults={'email': 'user1@test.com'})
if created:
    user1.set_password('user123')
    user1.save()
    print("Created user1 (is_staff=False)")
else:
    print("user1 already exists (is_staff={})".format(user1.is_staff))

# Create or update admin user
admin, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@test.com', 'is_staff': True, 'is_superuser': True})
if created:
    admin.set_password('admin123')
    admin.save()
    print("Created admin (is_staff=True)")
else:
    print("admin already exists (is_staff={})".format(admin.is_staff))

print("\nAll users:")
for u in User.objects.all():
    print(f"  {u.username}: is_staff={u.is_staff}")
