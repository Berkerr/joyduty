from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_object_link', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'text')

    def content_object_link(self, obj):
        from django.urls import reverse, NoReverseMatch # NoReverseMatch importu eklenebilir
        from django.utils.html import format_html

        # content_object'in varlığını ve content_type'ı kontrol et
        if obj.content_type and obj.content_object:
            try:
                # URL ismini dinamik olarak oluştur
                url_name = f'admin:{obj.content_type.app_label}_{obj.content_type.model}_change'
                # URL'yi bulmaya çalış
                admin_url = reverse(url_name, args=[obj.object_id])
                # Link oluştur
                return format_html('<a href="{}">{}</a>', admin_url, obj.content_object)
            except NoReverseMatch:
                # URL bulunamazsa, sadece nesneyi string olarak göster
                return str(obj.content_object)
        # Eğer content_object (veya content_type) yoksa N/A döndür
        return "N/A"
    content_object_link.short_description = 'Reviewed Object'
