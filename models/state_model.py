import requests
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class StateModel(models.Model):
    _name = 'state.model'
    _description = 'State Model'

    key = fields.Char(string='Key', required=True)
    val = fields.Char(string='Value', required=True)

    
class StatesModel(models.Model):
  
    _inherit = 'res.country.state'
    key = fields.Char(string='Key')
    district_ids = fields.One2many('district.model', 'state_id', string='Districts')
    
    
    @api.model
    def fetch_states(self):
        _logger.info("Starting state fetch process")
        url = "https://prime-iq.com/primeservices_dev/webapi/General/noLoginGetStates/NOLOGINGENERALINFO/PRIMECGENINFO3b87874lmkj44dfchc355r2022EXT"
        
        try:
            response = requests.get(url)
            _logger.info(f"API Response status: {response.status_code}")
            
            if response.status_code == 200:
                states = response.json()
                for state in states:
                    existing = self.search([('key', '=', state['key'])])
                    if not existing:
                        self.create({
                            'key': state['key'],
                            'name': state['val'],
                            'country_id': self.env.ref('base.iq').id
                        })
                        _logger.info(f"Created state: {state['val']}")
                    else:
                        _logger.debug(f"State exists: {state['val']}")
        except Exception as e:
            _logger.error(f"Error fetching states: {str(e)}")
        return True
    

