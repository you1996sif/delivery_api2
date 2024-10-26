from odoo import models, fields, api


class PartnerModel(models.Model):
    _inherit = 'res.partner'
    
    district_id = fields.Many2one('district.model', string='district', required=True)
    phone = fields.Char(string='Phone', required=True)
    street = fields.Char(string='Street', required=True)
    state_id = fields.Many2one('res.country.state', string='State', required=True)
    
    @api.depends('district_id')
    def _compute_city(self):
        for partner in self:
            if partner.district_id:
                partner.city = partner.district_id.district_id  
            else:
                partner.city = False  
