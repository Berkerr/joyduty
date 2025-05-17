# caravans/views.py
from django.shortcuts import render, get_object_or_404
# Review modelini ve ContentType'ı import et
from django.contrib.contenttypes.models import ContentType
from reviews.models import Review
from reviews.forms import ReviewForm # Yorum formunu import et
from django.conf import settings
from .models import CaravanModel, CaravanType, CaravanImage, CaravanEquipment
from brands.models import Brand

# BU FONKSİYONUN VAR OLDUĞUNDAN VE ADININ DOĞRU OLDUĞUNDAN EMİN OLUN
def caravan_list(request, type_slug=None, brand_slug=None):
    """
    Tüm onaylanmış karavanları, belirli bir tipe veya markaya ait olanları listeler.
    """
    caravan_type = None
    brand = None
    types = CaravanType.objects.all().order_by('name')
    caravans = CaravanModel.objects.filter(is_approved=True).select_related('brand', 'type').prefetch_related('images')

    if type_slug:
        caravan_type = get_object_or_404(CaravanType, slug=type_slug)
        caravans = caravans.filter(type=caravan_type)

    if brand_slug:
        brand = get_object_or_404(Brand, slug=brand_slug)
        caravans = caravans.filter(brand=brand)

    brands_with_caravans = CaravanModel.objects.filter(is_approved=True).values_list('brand__name', 'brand__slug').distinct()

    # Calculate review counts and average ratings for each caravan
    caravan_data = []
    for caravan in caravans:
        reviews = Review.objects.filter(
            content_type=ContentType.objects.get_for_model(caravan),
            object_id=caravan.pk
        )
        review_count = reviews.count()
        average_rating = None
        if reviews:
            total_rating = sum(review.rating for review in reviews if review.rating)
            average_rating = total_rating / len(reviews)
        caravan_data.append({
            'caravan': caravan,
            'review_count': review_count,
            'average_rating': average_rating
        })

    context = {
        'caravan_type': caravan_type,
        'types': types,
        'caravan_data': caravan_data, # Pass the list of dictionaries
        'brands_with_caravans': brands_with_caravans,
        'brand': brand,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'caravans/caravan_list.html', context)

def caravan_detail_by_slugs(request, brand_slug, model_slug):
    caravan = get_object_or_404(
        CaravanModel.objects.select_related('brand', 'type')
                       .prefetch_related(
                           'images',
                           'caravanequipment_set__equipment'
                       ),
        brand__slug=brand_slug,
        model_name__slug=model_slug,
        is_approved=True
    )

    # --- Yorumları Çekme ---
    content_type = ContentType.objects.get_for_model(caravan)
    reviews = Review.objects.filter(
        content_type=content_type,
        object_id=caravan.pk
    ).select_related('user').order_by('-created_at')

    # Calculate average rating
    if reviews:
        total_rating = sum(review.rating for review in reviews if review.rating)
        average_rating = total_rating / len(reviews)
    else:
        average_rating = None

    # --- Yorum Formunu Oluştur ---
    review_form = ReviewForm()

    # --- Context'i Güncelle ---
    all_equipment_items = caravan.caravanequipment_set.all()
    standard_equipment = [item for item in all_equipment_items if item.is_standard]
    optional_equipment = [item for item in all_equipment_items if not item.is_standard]

    context = {
        'caravan': caravan,
        'standard_equipment': standard_equipment,
        'optional_equipment': optional_equipment,
        'reviews': reviews,
        'review_form': review_form,
        'average_rating': average_rating,
    }
    return render(request, 'caravans/caravan_detail.html', context)

def caravan_detail_by_pk(request, pk):
    caravan = get_object_or_404(
        CaravanModel.objects.select_related('brand', 'type')
                       .prefetch_related(
                           'images',
                           'caravanequipment_set__equipment'
                       ),
        pk=pk,
        is_approved=True
    )

    # --- Yorumları Çekme ---
    # 1. CaravanModel için ContentType nesnesini al
    content_type = ContentType.objects.get_for_model(caravan)
    # 2. Bu content_type ve caravan'ın ID'si (object_id) ile eşleşen tüm Review'ları al
    #    İlişkili kullanıcıyı da önceden çekelim (select_related)
    reviews = Review.objects.filter(
        content_type=content_type,
        object_id=caravan.pk
    ).select_related('user').order_by('-created_at')

    # Calculate average rating
    if reviews:
        total_rating = sum(review.rating for review in reviews if review.rating)
        average_rating = total_rating / len(reviews)
    else:
        average_rating = None

    # --- Yorum Formunu Oluştur ---
    # Formu sadece GET isteği için burada oluşturuyoruz,
    # POST işlemi add_review view'ında ele alınacak.
    review_form = ReviewForm()

    # --- Context'i Güncelle ---
    all_equipment_items = caravan.caravanequipment_set.all()
    standard_equipment = [item for item in all_equipment_items if item.is_standard]
    optional_equipment = [item for item in all_equipment_items if not item.is_standard]

    context = {
        'caravan': caravan,
        'standard_equipment': standard_equipment,
        'optional_equipment': optional_equipment,
        'reviews': reviews,
        'review_form': review_form,
        'average_rating': average_rating,
    }
    return render(request, 'caravans/caravan_detail.html', context)
