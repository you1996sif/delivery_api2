from odoo import models, fields

class StateModel(models.Model):
    _name = 'state.model'
    _description = 'State Model'

    key = fields.Char(string='Key', required=True)
    val = fields.Char(string='Value', required=True)

    
class StatesModel(models.Model):
  
    _inherit = 'res.country.state'
    key = fields.Char(string='Key')
    

