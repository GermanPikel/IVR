from django.contrib import admin
from IVR_project.apps.IVR_web import models

admin.site.register(models.Timeline)
admin.site.register(models.Event)