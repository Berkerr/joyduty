from django.shortcuts import render
from itertools import chain
from operator import attrgetter
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib.contenttypes.models import ContentType
from django.views.generic import TemplateView # Import TemplateView

from accounts.models import Follower
from brands.models import Brand
from equipment.models import Equipment, EquipmentCategory
from caravans.models import CaravanModel, CaravanType
from reviews.models import Review
from locations.models import Location

def home_redirect_view(request):
    if request.user.is_authenticated:
        return home(request)
    else:
        return landing_page(request)

def home(request):
    latest_brands_list = list(Brand.objects.all().order_by('-id')[:15])
    latest_equipment_list = list(Equipment.objects.all().order_by('-id')[:15])
    latest_caravans_list = list(CaravanModel.objects.filter(is_approved=True).order_by('-id')[:15])
    latest_reviews_list = list(Review.objects.all().order_by('-created_at')[:15])
    latest_locations_list = list(Location.objects.filter(is_approved=True).order_by('-created_at')[:15])

    combined_items = list(chain(
        latest_brands_list,
        latest_equipment_list,
        latest_caravans_list,
        latest_reviews_list,
        latest_locations_list
    ))

    seen_ids = set()
    unique_items = []
    for item in combined_items:
        item_key = (item.__class__.__name__, item.pk)
        if item_key not in seen_ids:
            unique_items.append(item)
            seen_ids.add(item_key)

    from django.utils import timezone
    timeline_items_sorted = sorted(unique_items, key=lambda x: (getattr(x, 'created_at', timezone.now()), x.id), reverse=True)

    timeline_items_with_type = []
    for item in timeline_items_sorted[:10]:
        item_type = item.__class__.__name__
        timeline_items_with_type.append({
            'object': item,
            'item_type': item_type
        })

    User = get_user_model()
    current_user = request.user
    who_to_follow_users = User.objects.exclude(id=current_user.id).all()[:5]
    for user in who_to_follow_users:
        user.posts_count = Review.objects.filter(user=user).count()
        user.is_following = Follower.objects.filter(follower=current_user, following=user).exists()
        user.follower_count = user.followers.count()
        user.following_count = user.following.count()

    context = {
        'page_title': 'Home Feed',
        'timeline_items': timeline_items_with_type,
        'who_to_follow_users': who_to_follow_users,
        'current_user': current_user,
    }
    return render(request, 'core/home.html', context)

def map_view(request):
    return render(request, 'core/map.html')

def landing_page(request):
    # Fetch data for the Caravan section
    caravan_type = None
    try:
        caravan_type = CaravanType.objects.get(name="Karavan")
    except CaravanType.DoesNotExist:
        pass

    latest_caravans = CaravanModel.objects.filter(is_approved=True).order_by('-created_at')[:5]
    recently_updated_caravans = CaravanModel.objects.filter(is_approved=True).order_by('-updated_at')[:5]

    caravan_content_type = ContentType.objects.get_for_model(CaravanModel)

    recent_caravan_reviews = Review.objects.filter(
        content_type=caravan_content_type
    ).order_by('-created_at')[:5]

    caravans_with_recent_reviews = []
    seen_caravan_ids = set()
    for review in recent_caravan_reviews:
        caravan = review.content_object
        if caravan and caravan.id not in seen_caravan_ids:
            caravans_with_recent_reviews.append(caravan)
            seen_caravan_ids.add(caravan.id)

    # Fetch data for the Equipment section
    equipment_category = None
    try:
        equipment_category = EquipmentCategory.objects.get(name="Ekipman")
    except EquipmentCategory.DoesNotExist:
        pass

    latest_equipment = Equipment.objects.all().order_by('-created_at')[:5]

    equipment_content_type = ContentType.objects.get_for_model(Equipment)

    recent_equipment_reviews = Review.objects.filter(
        content_type=equipment_content_type
    ).order_by('-created_at')[:5]

    equipment_with_recent_reviews = []
    seen_equipment_ids = set()
    for review in recent_equipment_reviews:
        equipment = review.content_object
        if equipment and equipment.id not in seen_equipment_ids:
            equipment_with_recent_reviews.append(equipment)
            seen_equipment_ids.add(equipment.id)

    context = {
        'page_title': 'Welcome',
        'caravan_type': caravan_type,
        'latest_caravans': latest_caravans,
        'recently_updated_caravans': recently_updated_caravans,
        'caravans_with_recent_reviews': caravans_with_recent_reviews,
        'equipment_category': equipment_category,
        'latest_equipment': latest_equipment,
        'equipment_with_recent_reviews': equipment_with_recent_reviews,
    }
    return render(request, 'core/landing_page.html', context)

# Static pages views
class AboutView(TemplateView):
    template_name = 'static_pages/about.html'

class ContactView(TemplateView):
    template_name = 'static_pages/contact.html'

class PrivacyPolicyView(TemplateView):
    template_name = 'static_pages/privacy_policy.html'

class TermsOfServiceView(TemplateView):
    template_name = 'static_pages/terms_of_service.html'

about_view = AboutView.as_view()
contact_view = ContactView.as_view()
privacy_policy_view = PrivacyPolicyView.as_view()
terms_of_service_view = TermsOfServiceView.as_view()
