from odoo import models, fields



class DistrictModel(models.Model):
    _name = 'district.model'
    _description = 'District Model'
    _rec_name = 'district_name'

    district_id = fields.Integer(string='District ID', required=True)
    district_name = fields.Char(string='District Name', required=True)
    