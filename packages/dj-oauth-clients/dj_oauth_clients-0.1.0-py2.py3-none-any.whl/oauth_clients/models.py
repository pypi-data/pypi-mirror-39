# -*- coding: utf-8 -*-
import uuid
import requests
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.six import python_2_unicode_compatible
from model_utils.models import TimeStampedModel


@python_2_unicode_compatible
class Client(TimeStampedModel):
    uid = models.UUIDField(_("UID"), default=uuid.uuid4, unique=True)
    name = models.CharField(_("Name"), max_length=100, unique=True)
    client_id = models.CharField(_("Client id"), max_length=255, unique=True)
    client_secret = models.CharField(_("Client secret"), max_length=255)
    authorization_endpoint = models.URLField(_("Authorization endpoint"), max_length=255)
    token_endpoint = models.URLField(_("Token endpoint"), max_length=255, blank=True, default='')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.PROTECT)
    scope = models.CharField(_("Scope"), max_length=255, blank=True, default='read')

    class Meta:
        verbose_name = _("Oauth2 client")
        verbose_name_plural = _("Oauth2 clients")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.token_endpoint:
            self.token_endpoint = self.authorization_endpoint
        return super(Client, self).save(*args, **kwargs)

    @property
    def session_state_name(self):
        return str(self.uid)

    def start_authorization_url(self, request, redirect_url):
        redirect_url = request.build_absolute_uri(redirect_url)
        result = '{}?response_type=code&client_id={}&redirect_uri={}&scope={}&state={}'
        state = str(uuid.uuid4())
        request.session[self.session_state_name] = state
        result = result.format(self.authorization_endpoint, self.client_id, redirect_url, self.scope, state)
        return result

    def complete_authorization(self, request, redirect_url):
        state = request.GET['state']
        if request.session[self.session_state_name] != state:
            raise ValueError("Wrong oauth state.")
        del request.session[self.session_state_name]
        code = request.GET['code']
        token_url = '{}?grant_type=authorization_code&client_id={}&client_secret={}&redirect_uri={}&code={}'
        token_url = token_url.format(self.token_endpoint, self.client_id, self.client_secret, redirect_url, code)
        response = requests.post(token_url)
        data = response.json()
        access_token = AccessToken()
        access_token.client = self
        access_token.token_type = data['token_type']
        access_token.expires_in = data['expires_in']
        access_token.access_token = data['access_token']
        access_token.refresh_token = data['refresh_token']
        access_token.save()


class AccessToken(TimeStampedModel):
    client = models.ForeignKey(Client, verbose_name=_("Client"), on_delete=models.CASCADE)
    user_id = models.CharField(_("User id"), max_length=255, blank=True, default='')
    username = models.CharField(_("Username"), max_length=255, blank=True, default='')
    token_type = models.CharField(_("Token type"), max_length=255)
    expires_in = models.IntegerField(_("Expires in"))
    access_token = models.CharField(_("Access token"), max_length=255)
    refresh_token = models.CharField(_("Refresh token"), max_length=255)

    class Meta:
        verbose_name = _("Access token")
        verbose_name_plural = _("Access tokens")    

    def do_refresh_token(self):
        url = '{}?grant_type=refresh_token&refresh_token={}&client_id={}&client_secret={}&scope={}'
        url = url.format(self.client.token_endpoint, self.refresh_token, self.client.client_id,
            self.client.client_secret, self.client.scope)
        response = requests.post(url)
        data = response.json()
        self.token_type = data['token_type']
        self.expires_in = data['expires_in']
        self.access_token = data['access_token']
        self.refresh_token = data['refresh_token']
        self.save()
