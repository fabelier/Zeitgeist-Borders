# -*- coding: utf-8 -*-
import os
import logging

from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.events import subscriber
from pyramid.events import ApplicationCreated
from pyramid.httpexceptions import HTTPFound
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.view import view_config


logging.basicConfig()
log = logging.getLogger(__file__)

here = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append(here)
import zeitgeist_borders

@view_config(route_name='home', renderer='home.mako')
def home_view(request):
    if request.method == 'POST' and request.POST.get('query'):
        return {'query': request.POST['query'],
                'result':
                    zeitgeist_borders.google_instants(request.POST['query'])}
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

config.add_route('home', '/')

config.add_static_view('static', os.path.join(here, 'static'))

config.scan()

application = config.make_wsgi_app()
