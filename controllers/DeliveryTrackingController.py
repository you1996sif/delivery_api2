from odoo import http
from odoo.http import request, Response
import json

class DeliveryTrackingController(http.Controller):
    @http.route('/delivery/track/<string:invoice_number>', type='http', auth='public', website=True)
    def track_delivery(self, invoice_number, **kwargs):
        """Public endpoint for tracking delivery status"""
        # Search for the invoice
        invoice = request.env['account.move'].sudo().search([
            ('unique_number', '=', invoice_number)
        ], limit=1)

        if not invoice:
            return request.render('web.404')

        # Get the related stock picking
        stock_picking = request.env['stock.picking'].sudo().search([
            ('sale_id', '=', invoice.invoice_origin)
        ], limit=1)

        if not stock_picking:
            return request.render('web.404')

        # Prepare tracking data
        tracking_data = {
            'invoice_number': invoice_number,
            'customer_name': invoice.partner_id.name,
            'status': dict(stock_picking._fields['delivery_status'].selection).get(stock_picking.delivery_status, ''),
            'delivery_status': stock_picking.delivery_status,
        }

        # Add reason if status is postponed or returned
        if stock_picking.delivery_status == 'postponed' and stock_picking.postponed_reason:
            tracking_data['reason'] = dict(stock_picking._fields['postponed_reason'].selection).get(
                stock_picking.postponed_reason, '')
        elif stock_picking.delivery_status in ['return_to_sender', 'rtn_withagent', 'rtn_tostore'] and stock_picking.return_reason:
            tracking_data['reason'] = dict(stock_picking._fields['return_reason'].selection).get(
                stock_picking.return_reason, '')

        return request.render('your_module_name.delivery_tracking_template', tracking_data)

    @http.route('/api/delivery/track/<string:invoice_number>', type='http', auth='public')
    def track_delivery_api(self, invoice_number, **kwargs):
        """API endpoint for tracking delivery status"""
        # Search for the invoice
        invoice = request.env['account.move'].sudo().search([
            ('unique_number', '=', invoice_number)
        ], limit=1)

        if not invoice:
            response = json.dumps({'error': 'Invoice not found'})
            return Response(response, status=404, headers={'Content-Type': 'application/json'})

        # Get the related stock picking
        stock_picking = request.env['stock.picking'].sudo().search([
            ('sale_id', '=', invoice.invoice_origin)
        ], limit=1)

        if not stock_picking:
            response = json.dumps({'error': 'Delivery not found'})
            return Response(response, status=404, headers={'Content-Type': 'application/json'})

        # Prepare tracking data
        tracking_data = {
            'invoice_number': invoice_number,
            'customer_name': invoice.partner_id.name,
            'status': dict(stock_picking._fields['delivery_status'].selection).get(stock_picking.delivery_status, ''),
            'delivery_status': stock_picking.delivery_status,
        }

        # Add reason if status is postponed or returned
        if stock_picking.delivery_status == 'postponed' and stock_picking.postponed_reason:
            tracking_data['reason'] = dict(stock_picking._fields['postponed_reason'].selection).get(
                stock_picking.postponed_reason, '')
        elif stock_picking.delivery_status in ['return_to_sender', 'rtn_withagent', 'rtn_tostore'] and stock_picking.return_reason:
            tracking_data['reason'] = dict(stock_picking._fields['return_reason'].selection).get(
                stock_picking.return_reason, '')

        response = json.dumps({'data': tracking_data})
        return Response(response, status=200, headers={'Content-Type': 'application/json'})