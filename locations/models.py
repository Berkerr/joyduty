# locations/models.py

from django.urls import reverse
from django.db import models
from django.conf import settings
from django.utils.text import slugify # Kategori/Lokasyon slug'ı için gerekirse

# Lokasyon Kategorileri (Kamp Alanı, Karavan Parkı, Doğal Nokta vb.)
class LocationCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")
    slug = models.SlugField(max_length=120, unique=True, verbose_name="URL Slug")
    # icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="Icon Class (e.g., FontAwesome)") # Opsiyonel

    class Meta:
        verbose_name = "Location Category"
        verbose_name_plural = "Location Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('locations:list_by_category', kwargs={'category_slug': self.slug})

# Lokasyon Olanakları (WC, Su, Elektrik, Wifi vb.)
class LocationAmenity(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Amenity Name")
    # icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="Icon Class") # Opsiyonel

    class Meta:
        verbose_name = "Location Amenity"
        verbose_name_plural = "Location Amenities"
        ordering = ['name']

    def __str__(self):
        return self.name

# Ana Lokasyon Modeli
class Location(models.Model):
    name = models.CharField(max_length=200, verbose_name="Location Name")
    slug = models.SlugField(max_length=220, unique=True, blank=True, verbose_name="URL Slug") # İleride eklenebilir
    category = models.ForeignKey(
        LocationCategory,
        on_delete=models.SET_NULL, # Kategori silinirse lokasyonu silme, null yap
        null=True,
        blank=True, # Kategori seçimi zorunlu olmayabilir (örn: "Diğer")
        related_name='locations',
        verbose_name="Category"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    # Konum Bilgileri (Harita için temel)
    # DecimalField daha hassas kontrol sağlar
    latitude = models.DecimalField(
        max_digits=10, # Toplam basamak sayısı (noktadan önce + sonra) örn: 40.123456
        decimal_places=7, # Noktadan sonraki basamak sayısı
        null=True, # Başlangıçta boş olabilir
        blank=True,
        verbose_name="Latitude"
    )
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True,
        verbose_name="Longitude"
    )
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Address (Optional)") # Yaklaşık adres

    # Olanaklar (ManyToMany)
    amenities = models.ManyToManyField(
        LocationAmenity,
        blank=True, # Hiçbir olanak seçilmeyebilir
        related_name='locations',
        verbose_name="Amenities"
    )

    # Yönetim ve Kullanıcı Bilgisi
    is_approved = models.BooleanField(default=False, verbose_name="Approved") # Başlangıçta onaylanmamış olsun
    suggested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True, # Admin de ekleyebilir
        on_delete=models.SET_NULL, # Kullanıcı silinirse öneriyi silme
        related_name='suggested_locations',
        verbose_name="Suggested By"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # İleride resimler için ForeignKey (LocationImage modeli) eklenecek

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        try:
            # Try to use slug-based URL
            return reverse('locations:detail_by_slug', kwargs={'slug': self.slug})
        except:
            # Fallback to PK-based URL if slug-based fails
            try:
                return reverse('locations:detail_by_pk', kwargs={'pk': self.pk})
            except:
                return "#"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

# İleride: Lokasyon Resimleri
# class LocationImage(models.Model):
#    location = models.ForeignKey(Location, related_name='images', on_delete=models.CASCADE)
#    image = models.ImageField(upload_to='locations/images/')
#    # ...
