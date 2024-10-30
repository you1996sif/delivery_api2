import os
from odoo import models, fields, exceptions , _, api
import requests
from odoo.http import request, Response
from datetime import datetime, timedelta

import logging
_logger = logging.getLogger(__name__)



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    picking_return_deadline = fields.Datetime(
        string='Return Deadline',
        related='picking_ids.return_deadline',
        readonly=True,
        help='Deadline for customer to return the order'
    )
    
    remaining_return_days = fields.Integer(
        string='Days Left for Return',
        related='picking_ids.remaining_return_days',
        readonly=True,
        help='Number of days remaining to return the order'
    )
    
    can_be_returned = fields.Boolean(
        string='Can Be Returned',
        related='picking_ids.can_be_returned',
        readonly=True,
        help='Indicates if the order is still within return window'
    )

    def action_view_return_timer(self):
        self.ensure_one()
        return {
            'name': _('Return Timer'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'res_id': self.picking_ids.filtered(lambda p: p.delivery_date).id,
            'target': 'new',
        }