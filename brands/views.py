from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from reviews.models import Review
from reviews.forms import ReviewForm
from .models import Brand
from equipment.models import Equipment
from caravans.models import CaravanModel
from geo.models import Country
from .forms import BrandForm
from django.shortcuts import render, get_object_or_404, redirect

def brand_create(request):
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            brand = form.save(commit=False)
            brand.created_by = request.user
            brand.save()
            return redirect('brands:detail', slug=brand.slug)
    else:
        form = BrandForm()
    return render(request, 'brands/brand_form.html', {'form': form})



def brand_list(request):
    brands = Brand.objects.all()

    # Product type filtering
    product_type = request.GET.get('product_type')
    if product_type == 'caravans':
        brands = brands.filter(caravan_models__isnull=False).distinct()
    elif product_type == 'equipment':
        brands = brands.filter(equipments__isnull=False).distinct()

    # Country filtering
    country_id = request.GET.get('country')
    country_selected = None
    if country_id:
        country_selected = get_object_or_404(Country, pk=country_id)
        brands = brands.filter(country_of_origin=country_selected)

    brand_reviews = {}
    for brand in brands:
        content_type = ContentType.objects.get_for_model(brand)
        reviews = Review.objects.filter(
            content_type=content_type,
            object_id=brand.pk
        ).count()
        brand_reviews[brand.pk] = reviews

    # Country counts for filtering
    country_counts = {}
    for country in Country.objects.all():
        count = Brand.objects.filter(country_of_origin=country).count()
        if count > 0:
            country_counts[country] = count

    context = {
        'brands': brands,
        'brand_reviews': brand_reviews,
        'country_counts': country_counts,
        'product_type': product_type,
        'country_selected': country_selected,
    }
    return render(request, 'brands/brand_list.html', context)


def brand_detail(request, slug):
    brand = get_object_or_404(Brand, slug=slug)

    equipment = Equipment.objects.filter(brand=brand)
    caravans = CaravanModel.objects.filter(brand=brand)

    brand_content_type = ContentType.objects.get_for_model(Brand)
    equipment_content_type = ContentType.objects.get_for_model(Equipment)
    caravan_content_type = ContentType.objects.get_for_model(CaravanModel)

    brand_reviews = Review.objects.filter(
        content_type=brand_content_type,
        object_id=brand.pk
    ).select_related('user').order_by('-created_at')

    equipment_reviews = []
    for item in equipment:
        reviews = Review.objects.filter(
            content_type=equipment_content_type,
            object_id=item.pk
        ).select_related('user').order_by('-created_at')
        for review in reviews:
            equipment_reviews.append((review, item.name))

    caravan_reviews = []
    for item in caravans:
        reviews = Review.objects.filter(
            content_type=caravan_content_type,
            object_id=item.pk
        ).select_related('user').order_by('-created_at')
        for review in reviews:
            caravan_reviews.append((review, item.model_name))

    if brand_reviews:
        total_rating = sum(review.rating for review in brand_reviews if review.rating)
        average_rating = total_rating / len(brand_reviews)
    else:
        average_rating = None

    review_form = ReviewForm()

    context = {
        'brand': brand,
        'brand_reviews': brand_reviews,
        'equipment_reviews': equipment_reviews,
        'caravan_reviews': caravan_reviews,
        'review_form': review_form,
        'average_rating': average_rating,
        'equipment': equipment,
        'caravans': caravans,
    }

    return render(request, 'brands/brand_detail.html', context)
