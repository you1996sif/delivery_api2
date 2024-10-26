from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class PrimeModel(models.Model):
    _name = 'prime.model'
    _description = 'prime Model'
    _rec_name = 'invoice_id'

    inv_id = fields.Integer(string='Invoice ID', required=True, help="the invoice id in my system same as senderSystemCaseId and the key in the post_shipment_to_api")
    prime_pk = fields.Char(string='PK in Prime', required=True, help="the primary key in prime system and the value in the post_shipment_to_api")
    invoice_id = fields.Many2one('account.move', string='invoice name')

    @api.model
    def create_prime_records(self, response_data):
        """
        Create records in prime.model based on response data from external API.
        :param response_data: Dictionary where keys are 'inv_id' and values are 'prime_pk'.
        """
        for inv_id_str, prime_pk in response_data.items():
            inv_id = int(inv_id_str)  # Ensure the inv_id is an integer
            invoice_record = self.env['account.move'].search([('id', '=', inv_id)], limit=1)
            if not invoice_record:
                _logger.error('Invoice with ID %s not found.', inv_id)
                continue  # Skip this iteration if no invoice is found

            # Create a new record in prime.model
            self.create({
                'inv_id': inv_id,
                'prime_pk': str(prime_pk),
                'invoice_id': invoice_record.id  # Link to the invoice record
            })
            _logger.info('Record created for Invoice ID %s with Prime PK %s', inv_id, prime_pk)
