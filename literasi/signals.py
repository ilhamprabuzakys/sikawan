import os
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from .models import Literasi

@receiver(pre_delete, sender=Literasi)
def delete_dokumen_file(sender, instance, **kwargs):
    if instance.dokumen:
        if os.path.isfile(instance.dokumen.path):
            os.remove(instance.dokumen.path)