from django.shortcuts import render, redirect, get_object_or_404
from django.core.serializers import serialize # JSON için
from django.http import JsonResponse, HttpResponse # JSON ve geçici detay
from .models import Location, LocationCategory, LocationAmenity
from reviews.forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from reviews.forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages

def location_list(request, category_slug=None):
    """
    Tüm onaylanmış lokasyonları veya belirli bir kategoriye ait olanları listeler.
    Hem liste hem de harita için veri hazırlar.
    """
    category = None
    categories = LocationCategory.objects.all().order_by('name')

    # Sadece onaylanmış ve konumu (lat/lon) olanları al (harita için önemli)
    # İlişkili kategoriyi de çekelim
    locations_qs = Location.objects.filter(
        is_approved=True,
        latitude__isnull=False, # Enlemi olmayanları haritada gösteremeyiz
        longitude__isnull=False # Boylamı olmayanları haritada gösteremeyiz
    ).select_related('category')

    # Kategoriye göre filtreleme
    if category_slug:
        category = get_object_or_404(LocationCategory, slug=category_slug)
        locations_qs = locations_qs.filter(category=category)

    # Harita için lokasyon verilerini GeoJSON formatına benzer bir yapıda hazırlayalım
    # Leaflet'in kolayca kullanabileceği bir format
    locations_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(loc.longitude), float(loc.latitude)] # ÖNEMLİ: Önce Boylam, Sonra Enlem!
                },
                "properties": {
                    "id": loc.pk,
                    "name": loc.name,
                    # Detay sayfasına URL (get_absolute_url eklenmeli)
                    "url": loc.get_absolute_url() if hasattr(loc, 'get_absolute_url') else '#',
                    "category": loc.category.name if loc.category else "N/A",
                    # İleride resim eklenebilir: "image_url": loc.get_primary_image_url()
                }
            }
            for loc in locations_qs # Sadece filtrelenmiş ve konumu olanları al
        ]
    }


    context = {
        'category': category,       # Seçili kategori
        'categories': categories,   # Tüm kategoriler (sidebar için)
        'locations': locations_qs,  # Liste görünümü için QuerySet
        'locations_geojson': locations_geojson, # Harita için JSON verisi
    }
    return render(request, 'locations/location_list.html', context)


# --- Detay Sayfası View'ı (Şimdilik sadece PK bazlı ve geçici) ---
def location_detail_by_pk(request, pk):
    location = get_object_or_404(
        Location.objects.select_related('category').prefetch_related('amenities'),
        pk=pk,
        is_approved=True
    )
    review_form = ReviewForm()
    context = {
        'location': location,
        'review_form': review_form,
    }
    return render(request, 'locations/location_detail.html', context)

@login_required
def location_review_create(request, pk):
    location = get_object_or_404(Location, pk=pk, is_approved=True)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.content_type = ContentType.objects.get_for_model(Location)
            review.object_id = location.pk
            review.save()
            messages.success(request, "Review submitted successfully!")
            return redirect('locations:detail_by_pk', pk=pk)
        else:
            context = {'location': location, 'review_form': form}
            return render(request, 'locations/location_detail.html', context)
    else:
        review_form = ReviewForm()
        context = {'location': location, 'review_form': review_form}
        return render(request, 'locations/location_detail.html', context)
