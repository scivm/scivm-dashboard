from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from environment.models import Environment

class UserProfile(models.Model):
    user = models.ForeignKey(User, null=True, unique=True)
    favorite_env = models.ManyToManyField(Environment, related_name='favorited_by')

    def __unicode__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    user = kwargs.get('instance')
    if kwargs.get('created'):
        profile = UserProfile(user=user)
        profile.save()

def get_default_apikey(user):
    try:
        return user.apikey_set.filter(enabled=True)[0]
    except IndexError:
        return None

# monkey patch user
User.get_default_apikey = lambda self: get_default_apikey(self)

# profile creation
post_save.connect(create_profile, sender=User)

# workaround for https://github.com/toastdriven/django-tastypie/issues/937
@receiver(post_save, sender=User)
def create_user_api_key(sender, **kwargs):
     from apikey.models import create_api_key
     create_api_key(User, **kwargs)
