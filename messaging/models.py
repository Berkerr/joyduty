# messaging/models.py
from django.db import models
from django.conf import settings # AUTH_USER_MODEL için
from django.urls import reverse
from django.db.models import Max, Q # Son mesajı ve okunmamışları bulmak için

class Conversation(models.Model):
    """
    İki veya daha fazla kullanıcı arasındaki bir konuşmayı temsil eder.
    Başlangıçta birebir (2 kullanıcı) odaklanalım.
    """
    # ManyToManyField, 2 kullanıcıyı veya ileride grup sohbetini destekler.
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations',
        verbose_name="Participants"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) # Son mesajla güncellenebilir

    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        ordering = ['-updated_at'] # En son güncellenen konuşmalar başta

    def get_absolute_url(self):
        # Konuşma detay sayfasına link
        return reverse('messaging:conversation_detail', kwargs={'pk': self.pk})

    def get_other_participant(self, user):
        """ Birebir konuşmada diğer kullanıcıyı döndürür. """
        return self.participants.exclude(pk=user.pk).first()

    def get_last_message(self):
        """ Bu konuşmadaki son mesajı döndürür. """
        return self.messages.order_by('-timestamp').first() # messages related_name'i aşağıda tanımlanacak

    def __str__(self):
        # Katılımcıların isimlerini listelemek daha açıklayıcı olabilir
        usernames = ", ".join([user.username for user in self.participants.all()])
        # Veya birebir sohbet için:
        # participants_list = list(self.participants.all())
        # if len(participants_list) == 2:
        #     return f"Conversation between {participants_list[0].username} and {participants_list[1].username}"
        return f"Conversation ID: {self.pk} ({usernames})"


class Message(models.Model):
    """
    Bir konuşma içindeki tek bir mesajı temsil eder.
    """
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages', # Konuşma üzerinden mesajlara erişim: conversation.messages.all()
        verbose_name="Conversation"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # Gönderen silinirse mesajları da silinsin (veya SET_NULL?)
        related_name='sent_messages',
        verbose_name="Sender"
    )
    content = models.TextField(verbose_name="Content")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")
    is_read = models.BooleanField(default=False, verbose_name="Is Read?")

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['timestamp'] # Mesajları eskiden yeniye sırala

    def __str__(self):
        return f"From {self.sender.username} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

# --- Helper Manager (Opsiyonel ama Kullanışlı) ---
class ConversationManager(models.Manager):
    def get_or_create_personal_conversation(self, user1, user2):
        """ İki kullanıcı arasındaki birebir konuşmayı bulur veya oluşturur. """
        # Kullanıcıların aynı olmamasını kontrol et
        if user1 == user2:
            raise ValueError("Users cannot create a conversation with themselves.")

        # İki kullanıcıyı da içeren ve sadece 2 katılımcısı olan konuşmayı ara
        conversation = self.get_queryset().filter(participants=user1).filter(participants=user2).annotate(num_participants=models.Count('participants')).filter(num_participants=2).first()

        if conversation:
            return conversation, False # Bulundu, oluşturulmadı

        # Bulunamadıysa yeni konuşma oluştur
        conversation = self.create()
        conversation.participants.add(user1, user2)
        return conversation, True # Oluşturuldu

# Conversation modeline manager'ı ekle
# class Conversation(models.Model):
#    ... (alanlar) ...
#    objects = ConversationManager() # Manager'ı ekle
