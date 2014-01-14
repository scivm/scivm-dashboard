from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import (ApiKeyAuthentication,
    SessionAuthentication, MultiAuthentication)
from django.contrib.auth.models import User
from tastypie.bundle import Bundle
from django.conf.urls import url
from environment.models import Environment

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'

class EnvironmentResource(ModelResource):
    owner = fields.ForeignKey(UserResource, 'user', null=True, blank=True)

    class Meta:
        queryset = Environment.objects.all()
        resource_name = 'environment'
        authorization = Authorization()
        authentication = MultiAuthentication(
            ApiKeyAuthentication(), SessionAuthentication())
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'delete']
