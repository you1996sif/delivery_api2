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
    state_code = fields.Selection([
        ('NJF', 'النجف'), ('KRB', 'كربلاء'), ('BBL', 'بابل الحلة'),
        ('DWN', 'الديوانية'), ('BGD', 'بغداد'), ('DYL', 'ديالى'),
        ('BAS', 'البصرة'), ('AMA', 'العمارة ميسان'), ('SAH', 'صلاح الدين'),
        ('ANB', 'الأنبار/رمادي'), ('NAS', 'الناصرية ذي قار'), ('KOT', 'الكوت واسط'),
        ('SAM', 'السماوة المثنى'), ('KRK', 'كركوك'), ('SMH', 'السليمانيه'),
        ('ARB', 'اربيل'), ('DOH', 'دهوك'), ('MOS', 'موصل')
    ], string='State')
    
    @api.model
    def fetch_districts(self):
        _logger.info("Starting district fetch process")
        base_url = "https://prime-iq.com/primeservices_dev/webapi/General/noLoginGetDistrictsOfState/NOLOGINGENERALINFO/{}/PRIMECGENINFO3b87874lmkj44dfchc355r2022EXT"
        total_created = 0
        total_existing = 0
        
        for state_code, state_name in self._fields['state_code'].selection:
            _logger.info(f"Fetching districts for state: {state_name} ({state_code})")
            try:
                response = requests.get(base_url.format(state_code))
                _logger.info(f"API Response status for {state_code}: {response.status_code}")
                
                if response.status_code == 200:
                    districts = response.json()
                    _logger.info(f"Retrieved {len(districts)} districts for {state_code}")
                    
                    for district in districts:
                        existing = self.search([
                            ('district_id', '=', district['districtId']),
                            ('state_code', '=', state_code)
                        ])
                        
                        if not existing:
                            self.create({
                                'district_id': district['districtId'],
                                'district_name': district['districtName'],
                                'state_code': state_code
                            })
                            total_created += 1
                            _logger.debug(f"Created district: {district['districtName']} ({district['districtId']})")
                        else:
                            total_existing += 1
                            _logger.debug(f"District already exists: {district['districtName']} ({district['districtId']})")
                else:
                    _logger.error(f"Failed to fetch districts for {state_code}. Status code: {response.status_code}")
                    
            except Exception as e:
                _logger.error(f"Error fetching districts for {state_code}: {str(e)}")
                
        _logger.info(f"District fetch completed. Created: {total_created}, Already existing: {total_existing}")
        return True