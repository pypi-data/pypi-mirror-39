from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

from .base import BaseProvider
from ..template import template_inheritance
from ..util import split_app, merge_dicts, log
from ..uid import wuid

import io
from collections import namedtuple
import warnings
import logging


##################################################
###   Static File Provider Factory


def init_provider_factories(key='CONTENT_PROVIDERS'):
    '''Called from apps.py when setting up'''
    factories = []
    dmp = apps.get_app_config('django_mako_plus')
    for index, provider_def in enumerate(dmp.options.get(key, [])):
        fac = ProviderFactory(provider_def, '_django_mako_plus_providers_{}_{}_'.format(key, index))
        if fac.options['enabled']:  # providers can be disabled globally in settings (to run on debug or prod only, for example)
            factories.append(fac)
    return factories


class ProviderFactory(object):
    '''Creator for a given Provider definition in settings.py.'''
    def __init__(self, provider_def, cache_key):
        self.cache_key = cache_key
        self.options = {}
        try:
            self.provider_class = provider_def['provider']
        except KeyError:
            raise ImproperlyConfigured('The Django Mako Plus template OPTIONS were not set up correctly in settings.py; a CONTENT_PROVIDERS item is missing `provider`.')
        if isinstance(self.provider_class, str):
            self.provider_class = import_string(self.provider_class)
        if not issubclass(self.provider_class, BaseProvider):
            raise ImproperlyConfigured('The Django Mako Plus template OPTIONS were not set up correctly in settings.py; The `provider` value must be a subclass of django_mako_plus.BaseProvider.')
        self.options = merge_dicts(self.provider_class.default_options, provider_def)

    def instance_for_template(self, template):
        '''Returns a provider instance for the given template'''
        # Mako already caches template objects, so I'm attaching the instance to the template for speed during production
        try:
            return getattr(template, self.cache_key)
        except AttributeError:
            pass

        # create and cache (if in prod mode)
        app_config, template_file = split_app(template.filename)
        if app_config is None:
            raise ImproperlyConfigured("Could not determine the app for template {}. Is this template's app registered as a DMP app?".format(template.filename))
        instance = self.provider_class(app_config, template_file, self.options)
        if not settings.DEBUG:
            setattr(template, self.cache_key, instance)
        return instance



####################################################
###   Main runner


class ProviderRun(object):
    '''A run through the providers for tself and its ancestors'''
    def __init__(self, tself, version_id=None, group=None, factories=None):
        '''
        tself:      `self` object from a Mako template (available during rendering).
        version_id: hash/unique number to place on links
        group:      provider group to include (defaults to all groups if None)
        factories:  list of provider factories to run on each template (defaults to settings.py if None)
        '''
        dmp = apps.get_app_config('django_mako_plus')
        self.uid = wuid()           # a unique id for this run
        self.request = tself.context.get('request')
        self.context = tself.context
        if version_id is not None:
            warnings.warn('The `version_id` parameter in links() is deprecated in favor of automatic file hashes.')
        self.buffer = io.StringIO()
        # Create a table of providers for each template in the ancestry:
        #
        #     base.htm,      [ JsLinkProvider1, CssLinkProvider1, ... ]
        #        |
        #     app_base.htm,  [ JsLinkProvider2, CssLinkProvider2, ... ]
        #        |
        #     index.html,    [ JsLinkProvider3, CssLinkProvider3, ... ]
        factories = [
            pf
            for pf in (factories if factories is not None else dmp.provider_factories)
            if group is None or group == pf.options['group']
        ]
        self.template_providers = [
            [ pf.instance_for_template(template) for pf in factories ]
            for template in reversed(list(template_inheritance(tself)))
        ]
        # Column-specific data dictionaries are maintained as the template providers run
        # (one per provider column).  These allow the provider instances of a given
        # column to share data if needed.
        #
        #      column_data = [ { col 1 }      , { col 2 }      , ... ]
        self.column_data = [ {} for pf in factories ]


    def run(self):
        '''Performs the run through the templates and their providers'''
        # start() on tself (the last template in the list)
        for providers in self.template_providers[-1:]:
            for provider, data in zip(providers, self.column_data):
                provider.start(self, data)
        # provide() on the all provider lists in the chain
        for providers in self.template_providers:
            for provider, data in zip(providers, self.column_data):
                if log.isEnabledFor(logging.DEBUG):
                    log.debug('[%s] %s running', provider.template_file, provider.__class__.__qualname__)
                provider.provide(self, data)
        # finish() on tself (the last template in the list)
        for providers in self.template_providers[-1:]:
            for provider, data in zip(providers, self.column_data):
                provider.finish(self, data)


    def write(self, content):
        '''Provider instances use this to write to the buffer'''
        self.buffer.write(content)
        if settings.DEBUG:
            self.buffer.write('\n')


    def getvalue(self):
        '''Returns the buffer string'''
        return self.buffer.getvalue()
