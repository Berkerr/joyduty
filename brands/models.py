from django.db import models
from django.urls import reverse
from django.utils import timezone

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Brand Name")
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
        return reverse('brands:detail', kwargs={'slug': self.slug})

    def __str__(self):
        # Bu metod, bir Brand nesnesi print edildiğinde veya Admin'de göründüğünde
        # hangi bilginin gösterileceğini belirler.
        return self.name
