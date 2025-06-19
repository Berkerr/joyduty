from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from reviews.models import Review  # Review modelini import et
from .models import Inventory, Follower
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType # ContentType modelini import et

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def profile_view(request, username):
    user = get_object_or_404(User, username=username)

    # Kullanıcının gönderilerini al
    user_reviews = Review.objects.filter(user=user).order_by('-created_at')[:5] # Son 5 gönderi
    post_count = Review.objects.filter(user=user).count()

    # Takipçi ve takip edilen sayılarını al
    follower_count = user.followers.count()
    following_count = user.following.count()

    is_following = False
    if request.user.is_authenticated:
        is_following = Follower.objects.filter(follower=request.user, following=user).exists()

    # Her bir gönderi için ek bilgiler (başlık, kategori, toplam yorum sayısı)
    latest_contents = []
    for review in user_reviews:
        content_obj = review.content_object
        content_title = ""
        content_category = ""
        content_review_count = 0

        if content_obj:
            # Başlık
            if hasattr(content_obj, 'model_name'): # CaravanModel için
                content_title = content_obj.model_name
            elif hasattr(content_obj, 'name'): # Equipment veya diğerleri için
                content_title = content_obj.name
            else:
                content_title = str(content_obj) # Varsayılan olarak nesnenin string temsili

            # Kategori
            if hasattr(content_obj, 'type') and content_obj.type: # CaravanModel için
                content_category = content_obj.type.name
            elif hasattr(content_obj, 'category') and content_obj.category: # Equipment için
                content_category = content_obj.category.name
            else:
                content_category = "N/A" # Kategori yoksa

            # Toplam yorum sayısı
            content_type = ContentType.objects.get_for_model(content_obj)
            content_review_count = Review.objects.filter(
                content_type=content_type,
                object_id=content_obj.id
            ).count()

        latest_contents.append({
            'review': review,
            'content_title': content_title,
            'content_category': content_category,
            'content_review_count': content_review_count,
            'content_object_url': content_obj.get_absolute_url() if hasattr(content_obj, 'get_absolute_url') else '#'
        })

    context = {
        'user': user,
        'post_count': post_count,
        'follower_count': follower_count,
        'following_count': following_count,
        'is_following': is_following,
        'latest_contents': latest_contents, # Yeni eklenen içerik listesi
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def inventory_list_view(request):
    inventory = Inventory.objects.filter(user=request.user)
    context = {
        'inventory': inventory
    }
    return render(request, 'accounts/inventory_list.html', context)

from django.http import HttpResponseForbidden

def follow_user(request, username):
    if request.method == 'POST' and request.user.is_authenticated:
        user_to_follow = get_object_or_404(User, username=username)
        if request.user != user_to_follow:
            follower, created = Follower.objects.get_or_create(follower=request.user, following=user_to_follow)
            if not created:
                follower.delete()
        return redirect('accounts:profile' , username=username)  # Redirect back to the profile page
    else:
        return HttpResponseForbidden()

def logout_view(request):
    logout(request)
    return redirect('home')
