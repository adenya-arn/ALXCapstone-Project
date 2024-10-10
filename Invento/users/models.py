from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, username):
        if not email or not username:
            raise ValueError('email or password not provided')
        
        user = self.model(email= self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password, username):
        user = self.create_user(email=email, password=password, username=username)
        user.is_staff = True
        user.is_superuser = True 
        user.save(using=self._db)

        return user



class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='User Email')
    username = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']