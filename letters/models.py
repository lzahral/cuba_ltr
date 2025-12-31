from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class Letter(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_letters"
    )

    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_letters",
        null=True, blank=True  
    )
    subject = models.CharField(max_length=255, blank=True) 
    body = models.TextField(blank=True) 

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies"
    )
    
    is_draft = models.BooleanField(default=False)
    is_deleted_sender = models.BooleanField(default=False)
    is_deleted_recipient = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject
    
    
class LetterAttachment(models.Model):
    letter = models.ForeignKey(
        Letter, on_delete=models.CASCADE, related_name="attachments"
    )
    file = models.FileField(upload_to='uploads/letter_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    original_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Attachment for {self.letter.subject}"
    
    def save(self, *args, **kwargs):
        if not self.original_name and self.file:
            self.original_name = self.file.name
        super().save(*args, **kwargs)