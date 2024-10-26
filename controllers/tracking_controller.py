# controllers/tracking_controller.py
from odoo import http
from odoo.http import request

class DeliveryTrackingController(http.Controller):
    @http.route('/tracking/<string:tracking_code>', type='http', auth='public', website=True)
    def tracking_page(self, tracking_code, **kwargs):
        picking = request.env['stock.picking'].sudo().search([
            ('tracking_code', '=', tracking_code)
        ], limit=1)
        
        if not picking:
            return request.render('website.404')

        # Get status mappings
        status_dict = dict(picking._fields['delivery_status'].selection)
        postponed_dict = dict(picking._fields['postponed_reason'].selection)
        return_dict = dict(picking._fields['return_reason'].selection)
        
        return request.render('delivery_api.tracking_template', {
            'picking': picking,
            'delivery_status': status_dict.get(picking.delivery_status),
            'postponed_reason': postponed_dict.get(picking.postponed_reason),
            'return_reason': return_dict.get(picking.return_reason),
            'tracking_history': picking.tracking_history_ids,
            'website_url': request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        })