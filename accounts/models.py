from django.db import models
from django.contrib.auth.models import User
from blog.models import Article

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
    image = models.ImageField(verbose_name=' عکس کاربری')

    class Meta:
        verbose_name = 'حساب کاربری'
        verbose_name_plural = 'حساب های کاربری'

    def __str__(self):
        return self.user.username