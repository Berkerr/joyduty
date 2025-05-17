from django.db import models
from django.conf import settings # Kullanıcı modeline bağlanmak için
from brands.models import Brand
from equipment.models import Equipment
from django.utils.text import slugify
from django.urls import reverse

# Karavan Tipleri (Motokaravan, Çekme Karavan, Campervan vb.)
class CaravanType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Type Name")
    slug = models.SlugField(max_length=120, unique=True, verbose_name="URL Slug")
    # description = models.TextField(blank=True, null=True, verbose_name="Description") # Opsiyonel

    class Meta:
        verbose_name = "Caravan Type"
        verbose_name_plural = "Caravan Types"
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('caravans:list_by_type', kwargs={'type_slug': self.slug})


# Karavan Modeli
class CaravanModel(models.Model):
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT, # Markaya bağlı model varken markanın silinmesini engelle
        related_name='caravan_models',
        verbose_name="Brand"
    )
    model_name = models.CharField(max_length=150, verbose_name="Model Name")
    type = models.ForeignKey(
        CaravanType,
        on_delete=models.SET_NULL, # Tip silinirse modeli silme, null yap
        null=True,
        blank=True,
        related_name='caravan_models',
        verbose_name="Type"
    )
    year_start = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Production Start Year")
    year_end = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Production End Year (or leave blank if current)")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    # Temel Özellikler (Örnekler - Daha fazla eklenebilir)
    length_mm = models.PositiveIntegerField(null=True, blank=True, verbose_name="Length (mm)")
    width_mm = models.PositiveIntegerField(null=True, blank=True, verbose_name="Width (mm)")
    height_mm = models.PositiveIntegerField(null=True, blank=True, verbose_name="Height (mm)")
    max_weight_kg = models.PositiveIntegerField(null=True, blank=True, verbose_name="Max Weight (kg)")
    berths = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Number of Berths") # Yatak sayısı

    # Ekipmanlarla Many-to-Many İlişki (through ile)
    equipments = models.ManyToManyField(
        Equipment,
        through='CaravanEquipment', # İlişkiyi yönetecek ara model
        related_name='caravan_models',
        blank=True, # Bir modelin hiç ekipmanı olmayabilir (başlangıçta)
        verbose_name="Equipment"
    )

    # Yönetim Alanları
    is_approved = models.BooleanField(default=True, verbose_name="Approved") # Başlangıçta sadece admin ekleyecekse True olabilir
    # suggested_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='suggested_caravans') # Kullanıcı önerme için
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Caravan Model"
        verbose_name_plural = "Caravan Models"
        # Bir markanın aynı isimde birden fazla modeli olamasın (opsiyonel kısıtlama)
        unique_together = ('brand', 'model_name')
        ordering = ['brand__name', 'model_name'] # Önce marka, sonra model adına göre sırala

    def __str__(self):
        return f"{self.brand.name} {self.model_name}"
    def get_absolute_url(self):
        try:
            # Try to use slug-based URL
            return reverse('caravans:detail_by_slug', kwargs={
                'brand_slug': self.brand.slug,
                'model_slug': slugify(self.model_name) # Assuming you want a slugified model name
            })
        except Exception:
            # Fallback to PK-based URL if slug-based fails
            try:
                return reverse('caravans:detail_by_pk', kwargs={'pk': self.pk})
            except Exception:
                return "#"  # URL bulunamazsa
    def get_display_image(self):
        """
        Gösterilecek ana resmi (primary) veya hiç primary yoksa ilk resmi döndürür.
        Hiç resim yoksa None döndürür.
        """
        # İlişkili resimleri 'images' related_name'i ile çekiyoruz
        # Önce primary=True olanı bulmaya çalış
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary
        # Primary yoksa, herhangi bir ilk resmi döndür
        return self.images.first()

# Karavan Modeline Ait Resimler
class CaravanImage(models.Model):
    caravan_model = models.ForeignKey(
        CaravanModel,
        on_delete=models.CASCADE, # Model silinirse resimleri de sil
        related_name='images',    # Model üzerinden resimlere erişim: model.images.all()
        verbose_name="Caravan Model"
    )
    image = models.ImageField(upload_to='caravans/images/', verbose_name="Image")
    caption = models.CharField(max_length=200, blank=True, null=True, verbose_name="Caption") # Resim alt yazısı (opsiyonel)
    is_primary = models.BooleanField(default=False, verbose_name="Primary Image") # Ana resim mi?

    class Meta:
        verbose_name = "Caravan Image"
        verbose_name_plural = "Caravan Images"
        ordering = ['-is_primary', 'id'] # Önce ana resmi, sonra eklenme sırasına göre sırala

    def __str__(self):
        return f"Image for {self.caravan_model}"

# Karavan Modeli ile Ekipman Arasındaki İlişkiyi Tutan Ara Model (ManyToMany Through Model)
class CaravanEquipment(models.Model):
    caravan_model = models.ForeignKey(CaravanModel, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    is_standard = models.BooleanField(default=True, verbose_name="Is Standard?") # Standart mı, Opsiyonel mi?

    class Meta:
        verbose_name = "Caravan Equipment"
        verbose_name_plural = "Caravan Equipments"
        # Bir model için aynı ekipman birden fazla (hem standart hem opsiyonel gibi) eklenemesin
        unique_together = ('caravan_model', 'equipment')

    def __str__(self):
        status = "Standard" if self.is_standard else "Optional"
        return f"{self.caravan_model} - {self.equipment} ({status})"
