import odoo
from odoo import http
import re

class APIDatabaseMiddleware:
    def __init__(self):
        self.api_db = None
        self.api_pattern = re.compile(r'^/api/')

    def load_api_db(self):
        if self.api_db is None:
            self.api_db = odoo.tools.config.get('api_database')

    def process_request(self, request):
        if not self.api_db:
            self.load_api_db()

        if self.api_pattern.match(request.httprequest.path) and self.api_db:
            request.session.db = self.api_db

# Create an instance of the middleware
api_middleware = APIDatabaseMiddleware()

# Monkey-patch Odoo's HttpRequest to include our middleware
original_init = http.HttpRequest.__init__

def patched_init(self, *args, **kwargs):
    original_init(self, *args, **kwargs)
    api_middleware.process_request(self)

http.HttpRequest.__init__ = patched_init
