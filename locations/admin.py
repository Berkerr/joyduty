# locations/admin.py

from django.contrib import admin
from .models import LocationCategory, LocationAmenity, Location

@admin.register(LocationCategory)
class LocationCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(LocationAmenity)
class LocationAmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'address', 'is_approved', 'suggested_by', 'created_at')
    list_filter = ('is_approved', 'category', 'amenities') # Olanaklara göre de filtrele
    search_fields = ('name', 'description', 'address', 'suggested_by__username')
    list_editable = ('is_approved',) # Onay durumunu listeden değiştir
    readonly_fields = ('created_at', 'updated_at', 'suggested_by') # Öneren kişi değiştirilemez olmalı
    autocomplete_fields = ['category', 'amenities', 'suggested_by'] # Seçimleri kolaylaştır

    # Düzenleme sayfasındaki alanları gruplayalım
    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'description', 'address')
        }),
        ('Coordinates (Optional)', {
            'classes': ('collapse',), # Başlangıçta kapalı
            'fields': ('latitude', 'longitude'),
            'description': "Enter coordinates manually or use map (integration coming soon)."
        }),
        ('Amenities', {
            'fields': ('amenities',) # ManyToMany alanı
        }),
        ('Approval', {
            'fields': ('is_approved', 'suggested_by')
        }),
    )

    # Henüz resim inline'ı yok

    # Onaylama için admin action ekleyelim
    def approve_locations(self, request, queryset):
        queryset.update(is_approved=True)
    approve_locations.short_description = "Mark selected locations as approved"

    actions = [approve_locations] # Action'ı ekle