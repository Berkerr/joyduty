from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Conversation, Message
from django.contrib.auth import get_user_model
from django.db.models import Max, Q

User = get_user_model()

@login_required
def conversation_list(request):
    """
    Kullanıcının dahil olduğu tüm konuşmaları listeler.
    En son mesajı olan konuşmalar üstte görünür.
    """
    conversations = Conversation.objects.filter(participants=request.user).annotate(
        last_message_time=Max('messages__timestamp')
    ).order_by('-last_message_time')

    # Her konuşma için okunmamış mesaj sayısını hesapla (isteğe bağlı)
    # for conversation in conversations:
    #     conversation.unread_count = conversation.messages.filter(is_read=False).exclude(sender=request.user).count()

    return render(request, 'messaging/conversation_list.html', {'conversations': conversations})

@login_required
def conversation_detail(request, pk):
    """
    Belirli bir konuşmanın detayını ve mesajlarını gösterir.
    Yeni mesaj gönderme formunu içerir.
    """
    conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)
    messages = conversation.messages.all()

    # Mesajları okundu olarak işaretle (isteğe bağlı)
    # conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            # Konuşmanın updated_at alanını güncelle
            conversation.save() # auto_now=True sayesinde güncellenir
            return redirect('messaging:conversation_detail', pk=pk) # Sayfayı yenile

    return render(request, 'messaging/conversation_detail.html', {'conversation': conversation, 'messages': messages})

@login_required
def create_conversation(request, user_id):
    """
    Belirli bir kullanıcı ile yeni bir birebir konuşma başlatır veya mevcut olanı döndürür.
    """
    other_user = get_object_or_404(User, pk=user_id)

    # Kendi kendine mesaj göndermeyi engelle
    if request.user == other_user:
         # Hata mesajı göster veya başka bir sayfaya yönlendir
         return redirect('some_error_page') # veya kendi profil sayfası

    # Mevcut birebir konuşmayı bul veya oluştur
    conversation, created = Conversation.objects.get_or_create_personal_conversation(request.user, other_user)

    # Konuşma detay sayfasına yönlendir
    return redirect('messaging:conversation_detail', pk=conversation.pk)

@login_required
def send_message(request, pk):
    """
    Belirli bir konuşmaya mesaj gönderir (AJAX veya form POST ile kullanılabilir).
    """
    if request.method == 'POST':
        conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            conversation.save() # updated_at'i güncelle
            # Başarı yanıtı döndür (AJAX için JSON) veya detay sayfasına yönlendir
            return redirect('messaging:conversation_detail', pk=pk)
    # GET isteği veya geçersiz POST ise hata döndür veya başka bir şey yap
    return redirect('messaging:conversation_detail', pk=pk) # Hata durumunda detay sayfasına geri dön

@login_required
def mark_conversation_as_read(request, pk):
    """
    Belirli bir konuşmadaki kullanıcının mesajlarını okundu olarak işaretler.
    (AJAX ile kullanılabilir)
    """
    conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)
    # Kullanıcının alıcı olduğu ve okunmamış olan mesajları bul
    conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    # Başarı yanıtı döndür (AJAX için JSON)
    return redirect('messaging:conversation_detail', pk=pk) # veya JSON yanıtı
