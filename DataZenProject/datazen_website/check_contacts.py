#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'datazen_website.settings')
django.setup()

from main.models import Contact

contacts = Contact.objects.all()
print(f'Total contacts: {len(contacts)}')
for i, c in enumerate(contacts, 1):
    user_info = c.user.username if c.user else 'anonymous'
    print(f'{i}. {c.name} (user: {user_info}) [{c.status}] - {c.email}')
