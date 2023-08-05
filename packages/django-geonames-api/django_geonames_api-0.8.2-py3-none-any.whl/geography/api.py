# -*- coding: utf-8 -*-
# Copyright (C) 2012 ZERO GACHIS SAS - All Rights Reserved

r""" Geography API resources
"""

# Django imports
from django.conf.urls import url
from django.conf import settings
from django.http import Http404
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q

# Tastypie imports
from tastypie.resources import ModelResource, Resource
from tastypie.utils import trailing_slash

# Haystack imports
from haystack.query import SearchQuerySet

# Models imports
from .models import City

# Snippets imports
from .string_utils import searchalize


class CityResource(ModelResource):
    r""" City resource for the API
    """

    class Meta:
        queryset = City.objects.filter()
        include_resource_uri = False
        resource_name = 'city'
        paginator_class = Paginator

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)" % self._meta.resource_name +
                r"/(?P<search_start>[-+]?.*)" +
                r"%s$" % trailing_slash(), self.wrap_view('get_search'),
                name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):
        r""" Returns city around a defined location """

        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        limit = int(request.GET.get('limit', 20))
        offset = int(request.GET.get('offset', 0))
        page = (offset / limit) + 1

        # Do the query.
        sqs = SearchQuerySet()
        search = searchalize(kwargs.pop('search_start'))\
            .replace("-", " ")
        search_start = sqs.query.clean(search)

        sqs = sqs.models(City)\
            .filter(Q(name_exact__startswith=str(search_start)) |
                    Q(code__startswith=search_start))\
            .order_by('namelength', 'name', 'code')

        paginator = Paginator(sqs, limit)

        try:
            page = paginator.page(int(request.GET.get('page', page)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        objects = []

        if not offset:
            offset = (page.number - 1) * limit

        for result in page.object_list:
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'meta': {
                'limit': limit,
                'next': page.has_next(),
                'previous': page.has_previous(),
                'total_count': page.paginator.count,
                'offset': offset
            },
            'objects': objects,
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)

    def get_object_list(self, request):
        return super(CityResource, self).get_object_list(request)

    def dehydrate(self, bundle):

        # Vérification de la présence du pays
        try:
            bundle.data['country'] = bundle.obj.country.name.title()
        except AttributeError:
            bundle.data['country'] = ''

        # Vérification de la présence de la région
        try:
            bundle.data['region'] = bundle.obj.region.name
        except AttributeError:
            bundle.data['region'] = ''

        # Vérification de la présence du département
        try:
            bundle.data['department'] = bundle.obj.department.name
        except AttributeError:
            bundle.data['department'] = ''

        # Vérification de la présence de l'agglomération
        try:
            bundle.data['conurbation'] = bundle.obj.conurbation.name
        except AttributeError:
            bundle.data['conurbation'] = ''

        return bundle
