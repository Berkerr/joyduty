from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings # Import settings to link to AUTH_USER_MODEL

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Brand Name")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Keep the brand if the user is deleted
        null=True, # Allow null for existing brands or if creator is unknown
        blank=True, # Allow blank in forms
        related_name='created_brands', # Reverse relation name
        verbose_name="Created By"
    )
    slug = models.SlugField(max_length=120, unique=True, verbose_name="URL Slug")
    logo = models.ImageField(
        upload_to='brands/logos/',
        null=True,
        blank=True,
        verbose_name="Logo"
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Description"
    )
    website = models.URLField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Website"
    )
    country_of_origin = models.ForeignKey(
        'geo.Country',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Country of Origin"
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")

    class Meta:
        verbose_name = "Brand"          # Modelin tekil, okunabilir adı (Admin için)
        verbose_name_plural = "Brands" # Modelin çoğul, okunabilir adı (Admin için)
        ordering = ['name']             # Varsayılan sıralama (alfabetik)

    def get_absolute_url(self):
        if self.slug:
            return reverse('brands:detail', kwargs={'slug': self.slug})
        else:
            return reverse('brands:list')

    def __str__(self):
        # Bu metod, bir Brand nesnesi print edildiğinde veya Admin'de göründüğünde
        # hangi bilginin gösterileceğini belirler.
        return self.name
