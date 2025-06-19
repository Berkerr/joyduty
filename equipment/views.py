# equipment/views.py
from django.shortcuts import render, get_object_or_404, Http404, redirect
# Review modelini ve ContentType'ı import et
from django.contrib.contenttypes.models import ContentType
from reviews.models import Review
from reviews.forms import ReviewForm # Yorum formunu import et
from .models import Equipment, EquipmentCategory
from brands.models import Brand
from .forms import EquipmentForm

def equipment_create(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.created_by = request.user
            equipment.save()
            return redirect('equipment:detail_by_pk', pk=equipment.pk)
        else:
            print(form.errors)
    else:
        form = EquipmentForm()
    return render(request, 'equipment/equipment_form.html', {'form': form})

# BU FONKSİYONUN VAR OLDUĞUNDAN VE ADININ DOĞRU OLDUĞUNDAN EMİN OLUN
def equipment_list(request, category_slug=None, brand_slug=None):
    """
    Tüm ekipmanları, belirli bir kategoriye veya markaya ait ekipmanları listeler.
    """
    category = None
    brand = None
    categories = EquipmentCategory.objects.all()
    equipments = Equipment.objects.select_related('category', 'brand').all()

    if category_slug:
        category = get_object_or_404(EquipmentCategory, slug=category_slug)
        # Get the category and all its descendants
        descendant_categories = category.get_descendants(include_self=True)
        # Filter equipment belonging to the category or its descendants
        equipments = equipments.filter(category__in=descendant_categories)

    if brand_slug:
        brand = get_object_or_404(Brand, slug=brand_slug)
        equipments = equipments.filter(brand=brand)

    brands_with_equipment = Equipment.objects.values_list('brand__name', 'brand__slug').distinct()

    # Calculate review counts and average ratings for each equipment
    equipment_data = []
    for equipment in equipments:
        reviews = Review.objects.filter(
            content_type=ContentType.objects.get_for_model(equipment),
            object_id=equipment.pk
        )
        review_count = reviews.count()
        average_rating = None
        if reviews:
            total_rating = sum(review.rating for review in reviews if review.rating)
            average_rating = total_rating / len(reviews)
        equipment_data.append({
            'equipment': equipment,
            'review_count': review_count,
            'average_rating': average_rating
        })

    context = {
        'category': category,
        'categories': categories,
        'equipment_data': equipment_data, # Pass the list of dictionaries
        'brands_with_equipment': brands_with_equipment,
        'brand': brand,
    }
    return render(request, 'equipment/equipment_list.html', context)

# --- ORTAK FONKSİYON: Yorumları ve Benzer Ekipmanları Çekmek İçin ---
def _get_equipment_context(equipment):
    """ Verilen ekipman için yorumları ve benzer ekipmanları çeker. """
    content_type = ContentType.objects.get_for_model(equipment)
    reviews = Review.objects.filter(
        content_type=content_type,
        object_id=equipment.pk
    ).select_related('user').order_by('-created_at')

    similar_equipments = Equipment.objects.filter(
        category=equipment.category
    ).exclude(pk=equipment.pk).select_related('category', 'brand')[:4]

    # Calculate average rating
    if reviews:
        total_rating = sum(review.rating for review in reviews if review.rating)
        average_rating = total_rating / len(reviews)
    else:
        average_rating = None

    # Yorum formunu da burada oluşturalım
    review_form = ReviewForm()

    return {
        'equipment': equipment,
        'reviews': reviews,
        'similar_equipments': similar_equipments,
        'review_form': review_form,
        'average_rating': average_rating,
    }

def equipment_detail_by_slugs(request, category_slug, brand_slug, equipment_slug):
    print("equipment_detail_by_slugs is being called") # Debugging output
    try:
        equipment = Equipment.objects.select_related('category', 'brand').get(
            slug=equipment_slug,
            category__slug=category_slug,
            brand__slug=brand_slug
        )
    except Equipment.DoesNotExist:
        raise Http404("Equipment does not exist or URL parameters are incorrect.")

    # Ortak fonksiyonu kullanarak context'i al
    context = _get_equipment_context(equipment)

    # Get standard and optional caravan models
    equipment = Equipment.objects.prefetch_related('caravan_models__caravanequipment_set').get(
        slug=equipment_slug,
        category__slug=category_slug,
        brand__slug=brand_slug
    )
    standard_caravans = equipment.caravan_models.filter(caravanequipment__is_standard=True).distinct()
    optional_caravans = equipment.caravan_models.filter(caravanequipment__is_standard=False).distinct()

    # Debugging output
    print(f"Standard caravans for {equipment.name}: {standard_caravans}")
    print(f"Optional caravans for {equipment.name}: {optional_caravans}")

    # Add to context
    context['standard_caravans'] = standard_caravans
    context['optional_caravans'] = optional_caravans
    context['user_reported_caravans'] = [] # Placeholder for user-reported caravans

    return render(request, 'equipment/equipment_detail.html', context)

def equipment_detail_by_pk(request, pk):
    print("equipment_detail_by_pk is being called") # Debugging output
    equipment = get_object_or_404(Equipment.objects.select_related('category', 'brand'), pk=pk)

    # Ortak fonksiyonu kullanarak context'i al
    context = _get_equipment_context(equipment)

    # Get standard and optional caravan models
    equipment = Equipment.objects.prefetch_related('caravan_models__caravanequipment_set').get(pk=pk)
    standard_caravans = equipment.caravan_models.filter(caravanequipment__is_standard=True).distinct()
    optional_caravans = equipment.caravan_models.filter(caravanequipment__is_standard=False).distinct()

    # Debugging output
    print(f"Standard caravans for {equipment.name}: {standard_caravans}")
    print(f"Optional caravans for {equipment.name}: {optional_caravans}")

    # Add to context
    context['standard_caravans'] = standard_caravans
    context['optional_caravans'] = optional_caravans
    context['user_reported_caravans'] = [] # Placeholder for user-reported caravans

    return render(request, 'equipment/equipment_detail.html', context)
