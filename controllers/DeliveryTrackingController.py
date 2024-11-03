# File: controllers/DeliveryTrackingControllerr.py
from odoo import http
from odoo.http import request
from datetime import datetime

class DeliveryTrackingController(http.Controller):
    @http.route(['/delivery/track/<string:token>'], type='http', auth='public', website=True)
    def track_delivery(self, token, **kwargs):
        sale_order = request.env['sale.order'].sudo().search([('tracking_token', '=', token)], limit=1)
        if not sale_order:
            return """
                <div style="text-align: center; padding: 50px;">
                    <h3>Invalid tracking link</h3>
                    <p>The tracking information you're looking for could not be found.</p>
                </div>
            """
            
        try:
            # Get the related invoice
            invoice = request.env['account.move'].sudo().search([
                ('invoice_origin', '=', sale_order.name),
                ('move_type', '=', 'out_invoice')
            ], limit=1)
            
            # Get related picking
            picking = request.env['stock.picking'].sudo().search([
                ('origin', '=', sale_order.name),
                ('picking_type_code', '=', 'outgoing'),
                ('state', '!=', 'cancel')
            ], limit=1)
            
            values = {
                'order_name': sale_order.name,
                'delivery_status': dict(picking._fields['delivery_status'].selection).get(picking.delivery_status, 'Pending') if picking else 'No Delivery Found',
                'partner_name': sale_order.partner_id.name,
                'invoice_number': invoice.unique_number if invoice else 'Not Available',
                'invoice_date': invoice.invoice_date if invoice else None,
            }
                
            return request.render('delivery_api.delivery_tracking_template', values)
            
        except Exception as e:
            return f"""
                <div style="text-align: center; padding: 50px;">
                    <h3>Error loading tracking information</h3>
                    <p>Please try again later.</p>
                </div>
            """