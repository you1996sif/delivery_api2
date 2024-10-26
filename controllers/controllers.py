from odoo import http
from odoo.http import request, Response
import json
import os

import xmlrpc.client as xmlrpclib

import logging


_logger = logging.getLogger(__name__)

# API_KEY = os.getenv('API_KEY')
API_KEY = 'd2bca692-f508-48da-b471-039d53c13457-lo9aw8vkGjd-hNRuc4T8b0Vksez3kEe3uweYjWWhlUU'
# syscode = os.getenv('SYSCODE')

# def generate_api_key(length=32):
#   # Generate a secure random string of the specified length
#   return secrets.token_urlsafe(length)
class DeliveryAPIController(http.Controller):
    
    @http.route('/api/delivery/update_status', type='http', auth='public', methods=['POST'], csrf=False)
    def update_delivery_status(self, **kwargs):
      
        api_key = request.httprequest.headers.get('X-API-KEY')
        if api_key == API_KEY and (API_KEY and  api_key != None):
            
        # Attempt to parse JSON data
            try:
                data = json.loads(request.httprequest.data.decode('utf-8'))
                print('len(data)')
                print(len(data))
                print(data)
            except json.JSONDecodeError as e:
                response = json.dumps({'error': f'Invalid JSON: {str(e)}'})
                return Response(response, status=400, headers={'Content-Type': 'application/json'})
            # Extract parameters
            invoice_name = data.get('invoice_name')
            new_status = data.get('delivery_status')
            postponed_reason = data.get('postponed_reason')
            _logger.info('postponed_reason')
            _logger.info(postponed_reason)
            return_reason = data.get('return_reason')
            _logger.info('return_reason')
            _logger.info(return_reason)
            _logger.info('new_status')
            _logger.info(new_status)

            # Validate input
            if not new_status  or len(data)>4:
                response = json.dumps({'error': 'Delivery status is required'})
                return Response(response, status=400, headers={'Content-Type': 'application/json'})
            if not invoice_name :
                response = json.dumps({'error': 'Invoice name is required'})
                return Response(response, status=400, headers={'Content-Type': 'application/json'})
            

            # Search for the invoice
            invoice = request.env['account.move'].sudo().search([
                ('unique_number', '=', invoice_name)
                
            ], limit=1)

            if not invoice:
                response = json.dumps({'error': 'Invoice not found'})
                return Response(response, status=404, headers={'Content-Type': 'application/json'})

            # Search for the related stock picking
            stock_picking = request.env['stock.picking'].sudo().search([
                ('sale_id', '=', invoice.invoice_origin)
            ], limit=1)

            if not stock_picking:
                response = json.dumps({'error': 'Stock picking not found for this invoice'})
                return Response(response, status=404, headers={'Content-Type': 'application/json'})

            # Update the delivery status
            valid_statuses = dict(stock_picking._fields['delivery_status'].selection)
            
            _logger.info('valid_statuses')
            _logger.info(valid_statuses)
            if new_status in valid_statuses:
                _logger.info('if new_status in')
                _logger.info(new_status in valid_statuses)
                
                stock_picking.sudo().write({'delivery_status': new_status})

                # If status is "postponed", validate the reason
                if new_status == 'postponed':
                    _logger.info('i new_status == postponed')
                    valid_postponed_reasons = dict(stock_picking._fields['postponed_reason'].selection)
                    if postponed_reason != None:
                        _logger.info('postponed_reason != None')
                        if postponed_reason in valid_postponed_reasons:
                            _logger.info(' if postponed_reason in valid_postponed_reasons')
                            stock_picking.sudo().write({'postponed_reason': postponed_reason})
                        else:
                            _logger.info('else postponed_reason in valid_postponed_reasons')
                            response = json.dumps({'error': 'Invalid postponed reason'})
                            return Response(response, status=400, headers={'Content-Type': 'application/json'})

                # If status is "return", validate the reason
                if new_status in ['return_to_sender', 'rtn_withagent', 'rtn_tostore']:  # Add more return statuses if needed
                    _logger.info("s in ['return_to_sender', 'rtn_withagent', 'rtn_tostore']:")
                    valid_return_reasons = dict(stock_picking._fields['return_reason'].selection)
                 

                    if return_reason != None:
                        _logger.info('return_reason != None')
                        _logger.info('else postponed_reason in valid_postponed_reasons')
                        if return_reason in valid_return_reasons:
                            _logger.info(' if return_reason in valid_return_reasons:')
                            stock_picking.sudo().write({'return_reason': return_reason})
                        else:
                            _logger.info(' else return_reason in valid_return_reasons:')
                            response = json.dumps({'error': 'Invalid return reason'})
                            return Response(response, status=400, headers={'Content-Type': 'application/json'})
                    _logger.info('1111111111')
                _logger.info('2222222222222222')
                  

                response = json.dumps({'success': 'Delivery status updated successfully'})
                return Response(response, status=200, headers={'Content-Type': 'application/json'})
            else:
                _logger.info('3333333333333333')
                response = json.dumps({'error': 'Invalid delivery status'})
                return Response(response, status=400, headers={'Content-Type': 'application/json'})
        else:
            _logger.info('444444444444444')
            response = json.dumps({'error': 'Unauthorized'})
            return Response(response, status=401, headers={'Content-Type': 'application/json'})

