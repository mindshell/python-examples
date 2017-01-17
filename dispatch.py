#!/usr/bin/env python

import re
from flup.server.fcgi import WSGIServer
from webob import Response, Request

from webapp.globals import *
from webapp.show_error_page import show_error_page, show_too_busy_page
from webapp.report_error import report_error
from webapp.urls import urls

SITE_ON = True

# build a test response.
def test(request):
    response = Response()

    response.body  = '<h1>Test</h1>'
    response.body += '<p>' + request.path_info + '</p>'
    response.body += '<p>' + request.script_name + '</p>'
    response.body += '<p>' + request.url + '</p>'

    return response

# build "site offline" response.
def display_off_msg(request):
    response = Response()

    response.body = '<h1>This site is currently offline.</h1>'

    return response

def app(env, start_response):
    try:
        request = Request(env)

        if not SITE_ON:
            response = display_off_msg(request)
            return response(env, start_response)

        path_info = request.path_info

        # TODO: return url[path]()
        for regex, callback, klass in urls:
            match = re.search(regex, path_info)
            if match:
                c = callback(request)
                return c.response(env, start_response)

        response = test(request)
        return response(env, start_response)
    except WebsiteTooBusy, e:
        logging.error("WebsiteTooBusy exception raised")
        response = show_too_busy_page()
        return response(env, start_response)
    except Exception, e:
        logging.error(e, exc_info=1)
        logging.error(type(e))
        logging.error(e)

        if not APP_DEV:
            report_error(e)
        response = show_error_page()
        return response(env, start_response)

try:
    # Start the app.
    logging.info("Starting app...")

    wsgi_opts = {}
    wsgi_opts['debug'] = True
    WSGIServer(app, **wsgi_opts).run()
except Exception, e:
    logging.critical("w")
    logging.critical(e)
finally:
    logging.info("Add more logging here.")
    pass
