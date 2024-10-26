import odoo
from odoo import http
from odoo.http import Root, HttpRequest
import re

class APIDatabaseMiddleware:
    def __init__(self, app):
        self.app = app
        self.api_db = None
        self.api_pattern = re.compile(r'^/api/')

    def load_api_db(self):
        if self.api_db is None:
            self.api_db = odoo.tools.config.get('api_database')

    def __call__(self, environ, start_response):
        if not self.api_db:
            self.load_api_db()

        path_info = environ.get('PATH_INFO', '')
        
        if self.api_pattern.match(path_info) and self.api_db:
            # This is an API call, force the use of the specified database
            environ['HTTP_X_ODOO_DBFILTER'] = f'^{re.escape(self.api_db)}$'
            environ['PATH_INFO'] = path_info.replace(f'/{self.api_db}', '', 1)

        return self.app(environ, start_response)

# Monkey-patch Odoo's Root class to include our middleware
original_load_addons = Root.load_addons

def patched_load_addons(self):
    original_load_addons(self)
    self.dispatch = APIDatabaseMiddleware(self.dispatch)

Root.load_addons = patched_load_addons
