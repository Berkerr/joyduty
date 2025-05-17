from django.shortcuts import render # render fonksiyonunu import et
from itertools import chain
from operator import attrgetter

# Create your views here.

from brands.models import Brand
from equipment.models import Equipment
from caravans.models import CaravanModel
from reviews.models import Review
from locations.models import Location # Location modelini import et


def home(request):
    # Fetch latest items from each model (fetch a bit more than needed)
    latest_brands_list = list(Brand.objects.all().order_by('-id')[:15])
    latest_equipment_list = list(Equipment.objects.all().order_by('-id')[:15])
    latest_caravans_list = list(CaravanModel.objects.filter(is_approved=True).order_by('-id')[:15])
    latest_reviews_list = list(Review.objects.all().order_by('-created_at')[:15])
    latest_locations_list = list(Location.objects.filter(is_approved=True).order_by('-created_at')[:15]) # Filter approved locations

    # Combine all lists
    combined_items = list(chain(
        latest_brands_list,
        latest_equipment_list,
        latest_caravans_list,
        latest_reviews_list,
        latest_locations_list
    ))

    # Sort the combined list by ID descending as a proxy for recency
    # A more accurate sort would require consistent timestamp fields on all models
    # or adding annotations. Sorting by ID is simpler for now.
    # Ensure uniqueness in case an item somehow appears in multiple lists (unlikely here)
    # We sort by ID after combining
    seen_ids = set()
    unique_items = []
    for item in combined_items:
        # Simple check for uniqueness based on model type and pk
        item_key = (item.__class__.__name__, item.pk)
        if item_key not in seen_ids:
            unique_items.append(item)
            seen_ids.add(item_key)

    from django.utils import timezone
    # Sort unique items by created_at descending, using id as a fallback
    timeline_items_sorted = sorted(unique_items, key=lambda x: (getattr(x, 'created_at', timezone.now()), x.id), reverse=True)

    # Limit to the latest 50 items and add type information
    timeline_items_with_type = []
    for item in timeline_items_sorted[:50]:
        item_type = item.__class__.__name__ # Get type name here in the view
        timeline_items_with_type.append({
            'object': item,
            'item_type': item_type
        })

    context = {
        'page_title': 'Home Feed', # Updated page title
        'timeline_items': timeline_items_with_type, # Pass the list of dictionaries
        # Keep other context variables if needed elsewhere, or remove if not
        # 'latest_brands': latest_brands_list[:5], # Example if needed elsewhere
        # 'latest_equipment': latest_equipment_list[:5],
        # 'latest_caravans': latest_caravans_list[:5],
        # 'latest_reviews': latest_reviews_list[:5],
    }
    return render(request, 'core/home.html', context)


def map_view(request):
    return render(request, 'core/map.html')
