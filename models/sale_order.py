import os
from odoo import models, fields, exceptions , _, api
import requests
from odoo.http import request, Response
from datetime import datetime, timedelta

import logging
_logger = logging.getLogger(__name__)



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    last_delivery_id = fields.Many2one(
        'stock.picking',
        string='Latest Delivery',
        compute='_compute_last_delivery',
        store=True
    )
    
    return_deadline = fields.Datetime(
        string='انتهاء موعد الارجاع',
        related='last_delivery_id.return_deadline',
        store=True
    )
    
    remaining_return_days = fields.Integer(
        string='عدد الايام المتبقية للارجاع',
        related='last_delivery_id.remaining_return_days'
    )

    @api.depends('state')
    def _compute_last_delivery(self):
        for order in self:
            delivery = self.env['stock.picking'].search([
                ('origin', '=', order.name),
                ('state', '=', 'done'),
                ('picking_type_code', '=', 'outgoing')
            ], limit=1, order='date_done desc')
            order.last_delivery_id = delivery.id if delivery else False