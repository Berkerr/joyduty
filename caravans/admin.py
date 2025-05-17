from django.contrib import admin
from .models import CaravanType, CaravanModel, CaravanImage, CaravanEquipment

# Register your models here.

@admin.register(CaravanType)
class CaravanTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

# CaravanEquipment için Inline Admin (CaravanModel içinde görünecek)
class CaravanEquipmentInline(admin.TabularInline): # veya StackedInline
    model = CaravanEquipment
    # Hangi ekipmanların seçilebileceğini kolaylaştırmak için autocomplete
    autocomplete_fields = ['equipment']
    extra = 1 # Varsayılan olarak 1 boş ekipman ekleme satırı göster
    verbose_name = "Equipment"
    verbose_name_plural = "Equipments (Standard/Optional)"

# CaravanImage için Inline Admin (CaravanModel içinde görünecek)
class CaravanImageInline(admin.TabularInline): # veya StackedInline
    model = CaravanImage
    extra = 1 # Varsayılan olarak 1 boş resim ekleme satırı göster
    fields = ('image', 'caption', 'is_primary') # Gösterilecek ve düzenlenecek alanlar
    readonly_fields = ('image_preview',) # Resim önizlemesi için (aşağıda tanımlanacak)

    # Küçük resim önizlemesi
    def image_preview(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 150px;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Preview'


@admin.register(CaravanModel)
class CaravanModelAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'type', 'year_start', 'year_end', 'is_approved', 'created_at')
    list_filter = ('type', 'brand', 'is_approved', 'berths') # Filtreleme seçenekleri
    search_fields = ('model_name', 'brand__name', 'description') # Arama alanları
    autocomplete_fields = ['brand', 'type'] # Marka ve Tip seçimi için autocomplete
    list_editable = ('is_approved',) # Listeden onay durumunu hızlıca değiştirebilme

    # Düzenleme sayfasında alanları gruplama (opsiyonel ama düzenli gösterir)
    fieldsets = (
        (None, {
            'fields': ('brand', 'model_name', 'type', 'is_approved')
        }),
        ('Production & Specs', {
            'classes': ('collapse',), # Başlangıçta kapalı gelsin
            'fields': ('year_start', 'year_end', 'length_mm', 'width_mm', 'height_mm', 'max_weight_kg', 'berths')
        }),
        ('Description', {
            'fields': ('description',)
        }),
    )

    # Inline'ları admin sayfasına ekle
    inlines = [CaravanEquipmentInline, CaravanImageInline]

    # Opsiyonel: Ana resmi listede gösterme
    # def main_image_thumbnail(...): ...