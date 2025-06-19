# equipment/models.py

from django.db import models
from django.urls import reverse  # URL'leri tersine çevirmek için
from brands.models import Brand # Marka modelini import ediyoruz
from mptt.models import MPTTModel, TreeForeignKey # Import MPTT classes
from django.conf import settings # Import settings to link to AUTH_USER_MODEL

# Create your models here.

class EquipmentCategory(MPTTModel): # Inherit from MPTTModel
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name") # Corrected verbose_name
    slug = models.SlugField(max_length=120, unique=True, verbose_name="URL Slug")
    parent = TreeForeignKey( # Use TreeForeignKey
        'self',
        on_delete=models.SET_NULL, # Keep SET_NULL, or change to CASCADE if needed
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        verbose_name="Parent Category" # Corrected verbose_name
    )
    # icon_class = models.CharField(max_length=50, blank=True, null=True, verbose_name="FontAwesome Icon Class") # Opsiyonel

    class MPTTMeta:
        order_insertion_by = ['name'] # Order siblings by name

    class Meta:
        verbose_name = "Equipment Category" # Corrected verbose_name
        verbose_name_plural = "Equipment Categories" # Corrected verbose_name_plural
        # ordering = ['name'] # MPTT handles ordering via MPTTMeta

    def get_absolute_url(self):
        """
        Bu kategoriye ait ekipmanları listeleyen URL'yi döndürür.
        """
        return reverse('equipment:list_by_category', kwargs={'category_slug': self.slug})

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=200, verbose_name="Equipment Name")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Keep the equipment if the user is deleted
        null=True, # Allow null for existing equipment or if creator is unknown
        blank=True, # Allow blank in forms
        related_name='created_equipment', # Reverse relation name
        verbose_name="Created By"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    category = models.ForeignKey(
        EquipmentCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='equipments',
        verbose_name="Category"
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='equipments',
        verbose_name="Brand"
    )
    model_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="Model Number")
    image = models.ImageField(
        upload_to='equipment/images/',
        null=True,
        blank=True,
        verbose_name="Image"
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="Equipment Slug")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Equipment"
        verbose_name_plural = "Equipments"
        ordering = ['category__name', 'name'] # Kategori ismine göre sıralamak için __name kullandık

    def get_absolute_url(self):
        # Yeni slug tabanlı URL'yi oluşturmayı dene
        if self.slug and self.category and self.category.slug and self.brand and self.brand.slug:
             try:
                 # Yeni URL pattern'imizin adını ('equipment:detail_by_slugs') kullan
                 return reverse('equipment:detail_by_slugs', kwargs={
                     'category_slug': self.category.slug,
                     'brand_slug': self.brand.slug,
                     'equipment_slug': self.slug
                 })
             except Exception: # NoReverseMatch veya başka bir hata olabilir
                 pass # Fallback'e geç
        # Fallback olarak PK tabanlı URL'yi dene
        try:
            # PK tabanlı URL pattern'imizin adını ('equipment:detail_by_pk') kullan
            return reverse('equipment:detail_by_pk', kwargs={'pk': self.pk})
        except Exception:
            return "#" # Geçersiz link

    def __str__(self):
        # __str__ metodunda reverse çağrısı olmamalı.
        # Eğer marka veya kategori yoksa hata vermemesi için kontrol ekleyelim.
        parts = [self.name]
        if self.category:
            parts.append(f"Category: {self.category.name}")
        if self.brand:
            parts.append(f"Brand: {self.brand.name}")
        return " (".join(parts) + ")" if len(parts) > 1 else self.name
