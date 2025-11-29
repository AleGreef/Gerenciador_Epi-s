from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O e-mail deve ser definido.')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
  
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None

    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['cpf']

    def __str__(self):
        return self.first_name or self.email or f'Usuario ID: {self.pk}'