import requests
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)




class DistrictModel(models.Model):
    _name = 'district.model'
    _description = 'District Model'
    _rec_name = 'district_name'

    district_id = fields.Integer(string='District ID', required=True)
    district_name = fields.Char(string='District Name', required=True)
    state_id = fields.Many2one('res.country.state', string='State', required=True)
    
    @api.model
    def fetch_districts(self):
        _logger.info("Starting district fetch process")
        base_url = "https://prime-iq.com/primeservices_dev/webapi/General/noLoginGetDistrictsOfState/NOLOGINGENERALINFO/{}/PRIMECGENINFO3b87874lmkj44dfchc355r2022EXT"
        
        states = self.env['res.country.state'].search([('key', '!=', False)])
        for state in states:
            try:
                response = requests.get(base_url.format(state.key))
                _logger.info(f"API Response for {state.key}: {response.status_code}")
                
                if response.status_code == 200:
                    districts = response.json()
                    for district in districts:
                        existing = self.search([
                            ('district_id', '=', district['districtId']),
                            ('state_id', '=', state.id)
                        ])
                        if not existing:
                            self.create({
                                'district_id': district['districtId'],
                                'district_name': district['districtName'],
                                'state_id': state.id
                            })
                            _logger.info(f"Created district: {district['districtName']}")
            except Exception as e:
                _logger.error(f"Error fetching districts for {state.key}: {str(e)}")
        return True
    
    def unlink_zero_districts(self):
        _logger.info("Starting deletion of districts with ID 0")
        zero_districts = self.env['district.model'].search([('district_id', '=', 0)])
        
        if zero_districts:
            _logger.info(f"Found {len(zero_districts)} districts with ID 0")
            try:
                zero_districts.unlink()
                _logger.info("Successfully deleted districts with ID 0")
            except Exception as e:
                _logger.error(f"Error deleting districts: {str(e)}")
        else:
            _logger.info("No districts found with ID 0")
        
        return True