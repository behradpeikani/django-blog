from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile

def save_profile(sender, **kwargs):
    if kwargs['created']:
        p1 = Profile(user=kwargs['instance'])
        p1.save()

post_save.connect(save_profile, sender=User)