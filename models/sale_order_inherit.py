from odoo import models, fields, api
from werkzeug.urls import url_join
import uuid

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    tracking_token = fields.Char('Tracking Token', readonly=True, copy=False)
    
    def generate_tracking_link(self):
        """Generate a unique tracking token and return tracking URL"""
        for order in self:
            if not order.tracking_token:
                order.tracking_token = str(uuid.uuid4())
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            return {
                'type': 'ir.actions.act_url',
                'url': url_join(base_url, f'/delivery/track/{order.tracking_token}'),
                'target': 'new'
            }