from django.db import models
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid 
import os


# validasi nomor telepon
phone_regex = RegexValidator(
    r'^628[0-9]{11,14}$',
    message="Nomor telepon harus dimulai dengan '628' dan memiliki panjang 11 hingga 14 digit",
)

class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('user harus mempunyai email')
        
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user 

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.set_password(password)
        user.is_staff = True 
        user.is_superuser = True 

        user.save(using=self._db)
        return user

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=[('ADMIN','Admin'),('USER','User')])

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=14,
        unique=True,
    )

    objects = UserManager()

    is_active = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=False)  
    is_superuser = models.BooleanField(default=False)
  
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name
    

def equipment_image_file_path(instance,  filename):
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4}{ext}'

    return os.path.join('uploads', 'equipment', filename)

class Equipment(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    stock_available = models.PositiveIntegerField()
    image = models.ImageField(null=True, blank=True, upload_to=equipment_image_file_path)

    def __str__(self):
        return self.name

class Borrowing(models.Model):
    STATUS_CHOICES = (
        ('Peminjaman', 'Peminjaman'),
        ('Pengembalian', 'Pengembalian'),
    )

    created_at = models.DateTimeField(default=datetime.now)
    borrowing_until = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='equipment')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.equipment} {self.status}'

    def save(self, *args, **kwargs):
        # Check apakah peminjaman baru dibuat
        is_new_borrowing = self.pk is None

        super().save(*args, **kwargs)

        # Jika ini adalah peminjaman baru, kurangi stock_available
        if is_new_borrowing and self.status == 'Peminjaman':
            self.equipment.stock_available -= 1
            self.equipment.save()

        # Jika peminjaman dikembalikan, tambahkan stock_available
        if not is_new_borrowing and self.status == 'Pengembalian':
            self.equipment.stock_available += 1
            History.objects.create(
                created_by=self.created_by,
                borrowings=self,
                description=f'sudah dikembalikan untuk alat {self.equipment} oleh peminjam {self.user}'
            )

            self.equipment.save()

        # Buat catatan sejarah otomatis hanya jika ini adalah peminjaman baru
        if is_new_borrowing:
            History.objects.create(
                created_by=self.created_by,
                borrowings=self,
                description=f'telah dilakukan peminjaman oleh {self.user} untuk alat {self.equipment}'
            )

class History(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    borrowings = models.ForeignKey(Borrowing, on_delete=models.CASCADE, related_name='borrowings')
    description = models.TextField()

    def __str__(self):
        return self.description
    

    
