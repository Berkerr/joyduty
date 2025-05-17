from django.contrib import admin
from .models import EquipmentCategory, Equipment
from mptt.admin import DraggableMPTTAdmin # Import DraggableMPTTAdmin
from django.contrib import admin
from .models import EquipmentCategory, Equipment
from mptt.admin import DraggableMPTTAdmin # Import DraggableMPTTAdmin

# Register your models here.

@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(DraggableMPTTAdmin): # Inherit from DraggableMPTTAdmin
    list_display = ('tree_actions', 'indented_title', 'slug') # Use MPTT list_display
    list_display_links = ('indented_title',) # Link to the indented title
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)} # Keep prepopulated_fields for now
    mptt_level_indent = 20 # Adjust indentation if needed

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'model_no', 'image_thumbnail')
    list_filter = ('category', 'brand')
    search_fields = ('name', 'description', 'model_no', 'brand__name')
    autocomplete_fields = ['category', 'brand'] # Kategori ve Marka seçimini arama kutusuyla kolaylaştıralım

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs['queryset'] = EquipmentCategory.objects.all()
            if request.GET.get('category'):
                kwargs['queryset'] = kwargs['queryset'].filter(name__icontains=request.GET.get('category'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Resim önizlemesi için benzer bir metod
    def image_thumbnail(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<a href="{0}" target="_blank"><img src="{0}" style="max-height: 40px; max-width: 100px;" /></a>', obj.image.url)
        return "-"
    image_thumbnail.short_description = 'Image Preview'
