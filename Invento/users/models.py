from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class Id(models.Model):
    id_no = models.CharField(max_length=100, unique=True, primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id_no} -- {self.username} -- {self.created}'


class UserManager(BaseUserManager):
    def create_user(self, id_no, password, email):
        if not id_no or not email:
            raise ValueError('The id_no and email are required')
        id_instance = Id.objects.get(id_no=id_no)
        user = self.model(email=self.normalize_email(email), id_no=id_instance)
        user.set_password(password)
        user.save(using= self._db)

        return user

    def create_superuser(self, email, password, id_no):
        user = self.create_user(id_no=id_no, email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using= self._db)


        return user


class User(AbstractUser):
    id_no = models.OneToOneField(Id, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, unique=True)
    last_accessed = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    

    USERNAME_FIELD = 'id_no'
    REQUIRED_FIELDS = ['email']

