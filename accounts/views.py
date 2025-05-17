from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from reviews.models import Review  # Review modelini import et
from .models import Inventory
from django.contrib.auth.decorators import login_required

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

    # Kullanıcının gönderi sayısını al
    post_count = Review.objects.filter(user=user).count()

    # Takipçi ve takip edilen sayılarını al (basit örnek)
    follower_count = 0  # Gerçek uygulamada takipçi ilişkisi olmalı
    following_count = 0 # Gerçek uygulamada takip edilen ilişkisi olmalı

    context = {
        'user': user,
        'post_count': post_count,
        'follower_count': follower_count,
        'following_count': following_count,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def inventory_list_view(request):
    inventory = Inventory.objects.filter(user=request.user)
    context = {
        'inventory': inventory
    }
    return render(request, 'accounts/inventory_list.html', context)
