import os
from odoo import models, fields, exceptions , _, api
import requests
from odoo.http import request, Response
import html2text
import logging
from datetime import datetime, timedelta


_logger = logging.getLogger(__name__)


API_KEY = os.getenv('API_KEY')
# syscode = os.getenv('SYSCODE')
syscode =''

class StockPicking(models.Model):
  
    _inherit = 'stock.picking'

    DELIVERY_STATUS_SELECTION = [
        ('pending', 'Pending'),
        # ('picked_up', 'Picked Up'),
        # ('awaiting_dispatch', 'Awaiting Dispatch'),  
        # ('delivered', 'Delivered'),
        
        ('return_to_sender', 'أرجاع للزبون'),
        ('move_onway', 'إرجاع إلى عند المندوب'),
        ('toinstore', 'إرجاع الشحنات إلى المخزن'),
        ('return_to_store', 'إرجاع الى المخزن'),
        ('resend', 'إعادة إرسال'),
        ('retry_delivery', 'إعادة توصيل'),
        ('gave_to_customer', 'تسليم الراجع للعميل'),
        ('err_senddlv_succ', 'تسليم بنجاح'),#
        ('succdlv', 'تسليم بنجاح'),#
        ('sucs_dlv', 'تسليم بنجاح'),#
        ('part_succ', 'تسليم بنجاح جزئيا'),
        ('sucs_dlv_changeamt', 'تسليم بنجاح مع تغيير مبلغ الوصل'),#
        ('chnge_agent', 'تغيير المندوب'),
        ('dlv_afterfail', 'تم التسليم'),#
        ('err_senddlv_succ', 'تم التسليم بنجاح'),#
        ('rtn_withagent', 'راجع عند المندوب'),
        ('rtn_tostore', 'راجع للمخزن'),
        ('rtn_to_agent', 'عودة إلى قيد التوصيل'),
        ('go_back_tostore_resend', 'عودة الى داخل المخزن لاعادة الارسال'),
        ('go_to_rtn_instore', 'عودة الى شحنات راجعة في المخزن'),
        ('go_back_to_dlv', 'عودة الى قيد التوصيل'),
        ('postponed', 'مؤجل'),
        
        ]

     # New Postponed Reasons Selection
    POSTPONED_REASON_SELECTION = [
        ('cls', 'الطريق مغلق'),
        ('no_order', 'تم تغيير العنوان من قبل الزبون'),
        ('no_answer', 'تم التأجيل لرغبة الزبون'),
        ('away_noonetorcv', 'مسافر ولا يوجد من يستلم'),
        ('not_correct_size', 'مؤجل بسبب الحظر'),
        ('rcv_different_state', 'الزبون في غير محافظة'),
        ('ziara', 'مؤجل بسبب الزيارة'),
    ]

    # New Return Reasons Selection
    RETURN_REASON_SELECTION = [
        ('cls', 'مغلق'),
        ('denied', 'رفض الطلب'),
        ('no_order', 'لم يطلب'),
        ('no_answer', 'لم يرد'),
        ('away_noonetorcv', 'مسافر ولا يوجد من يستلم'),
        ('will_rcv_laterfromsndr', 'سيستلم الطلب لاحقا من المحل'),
        ('not_correct_size', 'القياس ليس المطلوب'),
        ('not_same_item', 'البضاعة ليست هي المطلوبة'),
        ('rcv_different_state', 'تحويل الى غير محافظة'),
        ('itms_rcv_already', 'يقول أستلمت الطلب'),
        ('cls_after_call', 'غلق الهاتف بعد الأتفاق'),
        ('phone_not_inservice', 'الهاتف غير داخل بالخدمة'),
        ('price_diff', 'رفض بسبب اختلاف السعر'),
        ('rcv_different_fde', 'تحويل الى غير منطقة'),
        ('no_we', 'لا يرد بعد الاتفاق'),
        ('bloc_k', 'الزبون حاظر المندوب'),
        ('damaged_goods', 'بضاعة تالفة'),
        ('prohibited_goods', 'بضاعة ممنوعة'),
        ('prohibited_w_s', 'حجم و وزن ممنوع'),
        ('incorrect_assignment', 'إسناد خاطئ'),
    ]

    delivery_status = fields.Selection(
        selection=DELIVERY_STATUS_SELECTION,
        string='Delivery Status',
        default='pending',
        help='Status of the delivery'
    )

    # New fields for postponed reasons and return reasons
    postponed_reason = fields.Selection(
        selection=POSTPONED_REASON_SELECTION,
        string='Postponed Reason',
        help='Reason for postponing the delivery'
    )

    return_reason = fields.Selection(
        selection=RETURN_REASON_SELECTION,
        string='Return Reason',
        help='Reason for returning the delivery'
    )
    

    def button_validate(self):
        
        if self.picking_type_code == 'incoming':
            return super(StockPicking, self).button_validate()
        else:
            shipment_data = self.prepare_shipment_data()
            token = self.get_AccessToken()
            print(token)
            print(self.post_shipment_to_api(shipment_data, token))
            if self.post_shipment_to_api(shipment_data, token):
                res = super(StockPicking, self).button_validate()
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'message': _("The shipment has been successfully sent to Prime."),
                        'type': 'success',
                        'sticky': False,
                    }
                }
            else:
                raise exceptions.UserError(_("Failed button_validate"))
        
          
    
    def get_AccessToken(self):
       
        url = "https://prime-iq.com/primeservices_dev/webapi/IntegrationWs/RequestReceiveAccessToken/GIGGI/rewuh34jedbdeMeGIGGIggantwzzzr344ffloxmed344xbpaxxrr2024/K33PthisHidden"
        response = requests.get(url)
        print('get_AccessToken')
        if response.status_code == 200:
            body_response = response.json()
            syscode = body_response['val']
            return syscode
        else:
            raise exceptions.UserError("Failed to get_AccessToken.")
           
        
    def post_shipment_to_api(self, shipment_data, token):
        base_url = "https://prime-iq.com/primeservices_dev/webapi/IntegrationWs/ReceiveCasesOtherSystem"
        str = "GIGGI"
        url = f"{base_url}/{str}/{token}"
        try:
            print("hihih")
            response = requests.post(url,json=shipment_data)
            print('response.status_codeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee ',response.status_code )
            _logger.info('Response status code: %d', response.status_code)
            if response.status_code == 200 and response is not None and len(response.json()) >= 1:
                
              
                body_response = response.json()
                self.env['prime.model'].create_prime_records(body_response)
              



                _logger.info('Shipment data sent successfully: %s', body_response)
                self.message_post(body="Shipment data sent successfully.")
                return True
            else:
                _logger.info('error body = : %s', body_response)
                error_msg = "Failed to send shipment data, shipment data error, please check the contact information(phone, street, state)  response.status_code: {}   ".format(response.status_code)
                raise exceptions.UserError(error_msg)
               
        
        except requests.exceptions.RequestException as e:
            raise exceptions.UserError("Error sending shipment data: %s", str(e))
                
    
    def prepare_shipment_data(self):
        
            invoice = self.env['account.move'].sudo().search([
                ('invoice_origin', '=', self.origin)
            ], limit=1)
            print('11')
            print('self.origin')
            print(self.origin)
            print('invoice')
            print(invoice)

            if not invoice:
                print('not')
                raise exceptions.UserError('No invoice found the invoice have not created yet')
                
               

       
            narration_plain = html2text.html2text(invoice.narration or '')
            print('ff')
         

       
            product_names = [
                line.product_id.name for line in invoice.invoice_line_ids if line.product_id
            ]

            # Determine shipment charge based on the state
            shipment_charge = 6000  # Default charge
            state_key = invoice.partner_id.state_id.key
            if state_key == 'BGD':
                shipment_charge = 5000

            # Prepare the shipment data
            shipment_data = [{
                "masterCustomerName": invoice.company_id.name,
                "senderName": invoice.company_id.name,
                "senderHp": '07753756668',
                "receiverName": invoice.partner_id.name,
                "receiverHp1": invoice.partner_id.phone or '',
                "receiverHp2": invoice.partner_id.mobile or '',
                "state": state_key,  # Use 'code' for correct state code
                "district": invoice.partner_id.district_id.district_id or '',  # Ensure it's valid
                "locationDetails": invoice.partner_id.street or '',
                "rmk": narration_plain,
                "qty": int(sum(line.quantity for line in invoice.invoice_line_ids)),
                "receiptAmt": int(invoice.amount_total),
                "shipmentCharge": shipment_charge,  # Set the determined shipment charge
                "custReceiptNoOri": int(invoice.unique_number),
                "productInfo": "Products: " + ', '.join(product_names),
                "senderSystemCaseId": invoice.id
            }]
            print('ff')


            _logger.info('Shipment data prepared successfully: %s', shipment_data)

            return shipment_data
    
    
    delivery_date = fields.Datetime(
        string='Delivery Date',
        readonly=True,
        copy=False,
        help='Date when the order was delivered to the customer'
    )
    
    return_deadline = fields.Datetime(
        string='انتهاء موعد الارجاع',
        compute='_compute_return_deadline',
        store=True,
        help='Deadline for customer to return the order (31 days from delivery)'
    )
    
    remaining_return_days = fields.Integer(
        string='عدد الايام المتبقية للارجاع',
        compute='_compute_remaining_return_days',
        help='Number of days remaining to return the order'
    )

    @api.depends('delivery_date')
    def _compute_return_deadline(self):
        for picking in self:
            if picking.delivery_date:
                picking.return_deadline = picking.delivery_date + timedelta(days=31)
            else:
                picking.return_deadline = False

    @api.depends('return_deadline')
    def _compute_remaining_return_days(self):
        now = fields.Datetime.now()
        for picking in self:
            if picking.return_deadline and picking.return_deadline > now:
                remaining = picking.return_deadline - now
                picking.remaining_return_days = remaining.days
            else:
                picking.remaining_return_days = 0

    def write(self, vals):
        if vals.get('delivery_status') in ['err_senddlv_succ', 'succdlv', 'sucs_dlv', 'dlv_afterfail']:
            if not self.delivery_date:
                vals['delivery_date'] = fields.Datetime.now()
        return super(StockPicking, self).write(vals)

# [{
#   "masterCustomerName": "My Company (San Francisco)",
#   "senderName": "My Company (San Francisco)",
#   "senderHp": "077********", 11 digit
#   "receiverName": "يوسف باسل",
#   "receiverHp1": "07753756668",
#   "receiverHp2": "",
#   "state": "BGD",###
#   "district": 1346,
#   "locationDetails": "شارع المنظمة",
#   "rmk": "Terms & Conditions: &lt;https://giggiblack.nova-iq.com/terms&gt;  \n\n",
#   "qty": 6,### int
#   "receiptAmt":1362,###int
#   "shipmentCharge": 6000,###int
#   "custReceiptNoOri": "INV/2024/00011",
#   "productInfo": "Products: Corner Desk Right Sit, Desk Combination",
#   "senderSystemCaseId": 32
# }]
