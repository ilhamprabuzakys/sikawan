from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

from masters.models import Provinsi, Kabupaten, Kecamatan, Desa

class Satker(models.Model):
    nama_satker = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    kabupaten = models.ForeignKey(Kabupaten, on_delete=models.SET_NULL, null=True, blank=True, related_name='satker')
    provinsi = models.ForeignKey(Provinsi, on_delete=models.SET_NULL, null=True, blank=True, related_name='satker')
    
    level = models.IntegerField(default=1)
    
    class Meta:
        ordering = ['nama_satker', ]
        verbose_name = 'Satuan Kerja'
        verbose_name_plural = 'Daftar Satuan Kerja'
    
    def __str__(self):
        return str(self.nama_satker)
        
class Profile(models.Model):
    ROLE_CHOICES = ( ('superadmin', 'Super Admin'), ('bnnp', 'BNNP'), ('bnnk', 'BNNK'), )
    
    satker = models.ForeignKey(Satker, on_delete=models.CASCADE, null=True, blank=True, related_name='list_profile')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(null=True, blank=True, max_length=20, choices=ROLE_CHOICES, default="bnnk")
    notelp  = models.CharField(max_length=20, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=True)
    
    avatar = models.ImageField(
        default='images/avatar.png', # default avatar
        upload_to='profile_avatars' # dir to store the image
    )

    class Meta:
        ordering = ['-updated_at', ]
        verbose_name = 'Profile User'
        verbose_name_plural = 'Daftar Profile User'
        
    def __str__(self):
        return f'{self.user.username} - Profile'

    def get_avatar(self):
        return f"{settings.MEDIA_URL}{str(self.avatar)}"

    def save(self, *args, **kwargs):
        # save the profile first
        super().save(*args, **kwargs)

        # resize the image
        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            # create a thumbnail
            img.thumbnail(output_size)
            # overwrite the larger image
            img.save(self.avatar.path)
            
class SatkerBNNP(models.Model):
    id = models.IntegerField(primary_key=True)
    satker_id = models.BigIntegerField()
    nama_satker = models.CharField(max_length=12)
    provinsi_id = models.BigIntegerField()
    jumlah_profil = models.BigIntegerField()
    
    class Meta:
        managed = False
        db_table = 'users_satker_bnnp'
        
    def __str__(self):
        return f'{self.id}_{self.satker_id} - {self.provinsi_id}: {self.nama_satker} Total : {self.jumlah_profil}'
            
class SatkerBNNK(models.Model):
    id = models.IntegerField(primary_key=True)
    satker_id = models.BigIntegerField()
    nama_satker = models.CharField(max_length=12)
    kabupaten_id = models.BigIntegerField()
    jumlah_profil = models.BigIntegerField()
    
    class Meta:
        managed = False
        db_table = 'users_satker_bnnk'
        
    def __str__(self):
        return f'{self.id}_{self.satker_id} - {self.kabupaten_id}: {self.nama_satker} Total : {self.jumlah_profil}'