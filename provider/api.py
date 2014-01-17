from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import (ApiKeyAuthentication,
    SessionAuthentication, MultiAuthentication)
from django.contrib.auth.models import User
from tastypie.bundle import Bundle
from django.conf.urls import url
from provider.models import Provider

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'

class ProviderResource(ModelResource):
    owner = fields.ForeignKey(UserResource, 'user', null=True, blank=True)

    class Meta:
        queryset = Provider.objects.all()
        resource_name = 'provider'
        authorization = Authorization()
        authentication = MultiAuthentication(
            ApiKeyAuthentication(), SessionAuthentication())
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'delete']