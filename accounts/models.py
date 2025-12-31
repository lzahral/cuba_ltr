from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image

# Create your models here.


# class Notification(models.Model):
#     recipient = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='notifications')
#     title = models.CharField(max_length=200)
#     message = models.TextField()
#     url = models.CharField(max_length=500, blank=True) 
#     read = models.BooleanField(default=False)
#     is_deleted = models.BooleanField(default=False)
#     created_at = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"{self.title} -> {self.recipient}"

# class AccessPermission (models.Model):
#     code = models.CharField(max_length=30)
#     title = models.CharField(max_length=30)

#     def __str__(self):
#         return self.title

class Profile(models.Model):
    avatar = models.ImageField(
        null=True, blank=True, verbose_name="avatar", upload_to='uploads/avatar/')
    phone_number = models.CharField(
        max_length=11, null=True, blank=True)
    address = models.TextField()
    ROLE_CHOICES = (
        ('user', 'User'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar:
            img = Image.open(self.avatar.path)

            width, height = img.size

            # 👇 اگر مربعی نبود
            if width != height:
                min_side = min(width, height)

                left = (width - min_side) / 2
                top = (height - min_side) / 2
                right = (width + min_side) / 2
                bottom = (height + min_side) / 2

                img = img.crop((left, top, right, bottom))

            # 👇 (اختیاری) resize به 300x300
            img = img.resize((300, 300), Image.LANCZOS)

            img.save(self.avatar.path)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    # def is_admin(self):
    #     return self.user.groups.filter(name='admin').exists()

    # def is_manager(self):
    #     return self.user.groups.filter(name='manager').exists()


