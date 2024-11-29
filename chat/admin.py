from django.contrib import admin
from .models import Message

# Register the Message model to make it available in the Django admin interface
admin.site.register(Message)
