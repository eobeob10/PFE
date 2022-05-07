from .models import Documents
from .models import Scan
from django.contrib import admin
from django.contrib.auth.models import User

# admin.site.register(User)

admin.site.register(Scan)
admin.site.register(Documents)
