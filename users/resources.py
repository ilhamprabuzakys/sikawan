from django.contrib.auth.models import User
from import_export import resources

from . import models

class UserResource(resources.ModelResource):
    class Meta:
        model = User

class SatkerResource(resources.ModelResource):
    class Meta:
        model = models.Satker