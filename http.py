#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Zeitgeist Borders (https://github.com/fabelier/Zeitgeist-Borders/) 
# Developed by Antoine Mazières, Samuel Huron and Julien Palard.
# Contact : admin at fabelier dot org
#
# Zeitgeist Borders is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Zeitgeist Borders is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zeitgeist Borders.  If not, see <http://www.gnu.org/licenses/>.

import os
import logging
from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.events import subscriber
from pyramid.events import ApplicationCreated
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.view import view_config
from pyramid.renderers import JSONP


logging.basicConfig()
log = logging.getLogger(__file__)

here = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append(here)
import zeitgeist_borders
from cctld import cctlds


@view_config(route_name='home', renderer='home.mako')
def home_view(request):
    if request.method == 'POST' and request.POST.get('query'):
        return {'query': request.POST['query'],
                'result':
                    zeitgeist_borders.google_instants(request.POST['query'])}
    else:
        return {}


@view_config(route_name='search', renderer='search.mako')
@view_config(route_name='search_json', renderer='jsonp')
def search_view(request):
    if request.method == 'GET' and 'q' in request.GET:
        return {'query': request.GET['q'],
                'countries': dict((v, k)
                                  for k, v
                                  in cctlds.iteritems()),
                'result':
                    zeitgeist_borders.google_instants(request.GET['q'])}
    else:
        return {}


@view_config(context='pyramid.exceptions.NotFound', renderer='notfound.mako')
def notfound_view(self):
    return {}


@subscriber(NewRequest)
def new_request_subscriber(event):
    pass


@subscriber(ApplicationCreated)
def application_created_subscriber(event):
    pass

session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')

settings = {"mako.directories": os.path.join(here, "templates"),
            "mako.input_encoding": 'utf-8'}
config = Configurator(settings=settings, session_factory=session_factory)
config.include('pyramid_mako')
config.add_renderer('jsonp', JSONP(param_name='callback'))
config.add_route('home', '/')
config.add_route('search', '/search/')
config.add_route('search_json', '/search.json')

config.add_static_view('static', os.path.join(here, 'static'))

config.scan()

application = config.make_wsgi_app()

if __name__ == "__main__":
    from paste.httpserver import serve
    app = config.make_wsgi_app()
    serve(app, host='0.0.0.0', port='8085')
