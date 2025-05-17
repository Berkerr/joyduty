from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator # Rating için

# Create your models here.

class Review(models.Model):
    # Generic Foreign Key Alanları
    # Hangi model türüne ait olduğunu tutar (CaravanModel, Equipment, Location vb.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # İlgili modelin primary key'ini (ID) tutar
    object_id = models.PositiveIntegerField()
    # Yukarıdaki iki alanı kullanarak asıl nesneye ulaşmayı sağlayan sanal alan
    content_object = GenericForeignKey('content_type', 'object_id')

    # Yorumu Yapan Kullanıcı
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # Kullanıcı silinirse yorumları da silinsin
        related_name='reviews',   # Kullanıcı üzerinden yorumlara erişim: user.reviews.all()
        verbose_name="User"
    )

    # Yorum İçeriği
    text = models.TextField(verbose_name="Review Text")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], # 1-5 arası değerler
        null=True,  # Puanlama zorunlu olmayabilir
        blank=True, # Formda boş bırakılabilir
        verbose_name="Rating (1-5)"
    )

    # Zaman Damgaları
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At") # Düzenleme için

    # İleride eklenebilir: is_approved (moderasyon için)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        # En yeni yorumlar başta görünsün
        ordering = ['-created_at']
        # Generic Foreign Key alanlarında birlikte index oluşturmak performansı artırır
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        # Admin panelinde veya loglarda daha açıklayıcı görünüm
        return f"Review by {self.user.username} on {self.content_object} ({self.created_at.strftime('%Y-%m-%d')})"