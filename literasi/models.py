from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from . import validators

class Literasi(models.Model):
    STATUS_CHOICES = {
        ("draft", "DRAFT"),
        ("published", "PUBLISHED"),
        ("archived", "ARCHIVED"),
    }

    KATEGORI_CHOICES = {
        ("buku", "Buku"),
        ("audio", "Audio"),
        ("video", "Video"),
        ("video_youtube", "Video Youtube"),
    }
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="literasi_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="literasi_updated_by")
    
    dokumen = models.FileField(upload_to="upload/files/literasi", null=True, validators=[validators.validate_file_extension])
    judul = models.CharField(max_length=255)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="draft")
    kategori = models.CharField(max_length=15, choices=KATEGORI_CHOICES, default="buku")
    
    jumlah_diunduh = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-updated_at', ]
        verbose_name = 'Literasi'
        verbose_name_plural = 'Daftar Literasi'

    def __str__(self):
        return f'{self.judul} ({self.get_status_display()})'

    def get_absolute_url(self):
        return reverse("literasi_literasi_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("literasi_literasi_update", args=(self.pk,))