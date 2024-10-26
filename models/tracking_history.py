# models/tracking_history.py
from odoo import models, fields

class StockPickingTrackingHistory(models.Model):
    _name = 'stock.picking.tracking.history'
    _description = 'Delivery Tracking History'
    _order = 'create_date DESC'

    picking_id = fields.Many2one('stock.picking', string='Stock Picking', required=True)
    status = fields.Selection(selection=[
        ('pending', 'Pending'),
       
        
        ('return_to_sender', 'أرجاع للزبون'),
        ('move_onway', 'إرجاع إلى عند المندوب'),
        ('toinstore', 'إرجاع الشحنات إلى المخزن'),
        ('return_to_store', 'إرجاع الى المخزن'),
        ('resend', 'إعادة إرسال'),
        ('retry_delivery', 'إعادة توصيل'),
        ('gave_to_customer', 'تسليم الراجع للعميل'),
        ('err_senddlv_succ', 'تسليم بنجاح'),
        ('succdlv', 'تسليم بنجاح'),
        ('sucs_dlv', 'تسليم بنجاح'),
        ('part_succ', 'تسليم بنجاح جزئيا'),
        ('sucs_dlv_changeamt', 'تسليم بنجاح مع تغيير مبلغ الوصل'),
        ('chnge_agent', 'تغيير المندوب'),
        ('dlv_afterfail', 'تم التسليم'),
        ('err_senddlv_succ', 'تم التسليم بنجاح'),
        ('rtn_withagent', 'راجع عند المندوب'),
        ('rtn_tostore', 'راجع للمخزن'),
        ('rtn_to_agent', 'عودة إلى قيد التوصيل'),
        ('go_back_tostore_resend', 'عودة الى داخل المخزن لاعادة الارسال'),
        ('go_to_rtn_instore', 'عودة الى شحنات راجعة في المخزن'),
        ('go_back_to_dlv', 'عودة الى قيد التوصيل'),
        ('postponed', 'مؤجل'),
   
], string='Status')
    reason = fields.Char(string='Reason')
    reason_type = fields.Selection([
        ('postponed', 'Postponed'),
        ('return', 'Return'),
    ], string='Reason Type')
    create_date = fields.Datetime(string='Date', readonly=True)