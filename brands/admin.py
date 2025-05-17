from django.contrib import admin
from .models import Brand  # Kendi modellerimizi import ediyoruz

# Register your models here.

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'website', 'country_of_origin', 'logo_thumbnail') # Listede görünecek alanlar
    search_fields = ('name', 'website')                     # Arama yapılacak alanlar
    prepopulated_fields = {'slug': ('name',)}                # 'name' alanına yazınca 'slug' otomatik dolsun

    # Logoyu listede küçük göstermek için özel bir metod (opsiyonel ama güzel)
    def logo_thumbnail(self, obj):
        from django.utils.html import format_html
        if obj.logo:
            # Resmin üzerine tıklayınca orijinal boyutu yeni sekmede açsın
            return format_html('<a href="{0}" target="_blank"><img src="{0}" style="max-height: 40px; max-width: 100px;" /></a>', obj.logo.url)
        return "-" # Logo yoksa tire (-) göster
    logo_thumbnail.short_description = 'Logo Preview' # Kolon başlığı


# Alternatif (daha basit) kayıt yöntemi:
# admin.site.register(Brand)
# Bu yöntem yukarıdaki gibi özelleştirmelere izin vermez ama hızlıdır.
# Şimdilik @admin.register dekoratörünü kullanalım.
