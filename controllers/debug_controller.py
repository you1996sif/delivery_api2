from odoo import http

class DebugController(http.Controller):
    @http.route('/debug/test', auth='public')
    def debug_test(self):
        return "Debug route working"
