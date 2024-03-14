from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import KawasanRawan


@receiver(post_save, sender=KawasanRawan)
def update_desa_on_kawasan_rawan_change(sender, instance, created, **kwargs):
    if instance.desa and instance.desa.kecamatan:
        instance.desa.updated_at = timezone.now()
        # instance.desa.save(update_fields=['updated_at'])
        instance.desa.save(update_fields=[])
