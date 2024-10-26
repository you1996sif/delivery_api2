from odoo import models, fields, api

class AccountMoveExtended(models.Model):
    _inherit = 'account.move'

    unique_number = fields.Char(string='Unique Number', readonly=True, index=True)

   

    @api.model
    def create(self, vals):
        if 'unique_number' not in vals or not vals['unique_number']:
            print('ifffffffffffffffffffffffffffffffffffffffffffffffffffff')
            # Check if any record already exists
            last_record = self.search([], order='id desc', limit=1)
            if last_record:
                print('1111111111ifffffffffffffffffffffffffffffffffffffffffffffffffffff')
                # If there are existing records, continue from the last unique_number
                last_number = int(last_record.unique_number)
                next_number = last_number + 1
                vals['unique_number'] = str(next_number).zfill(6)
                print(vals)
                result = super(AccountMoveExtended, self).create(vals)
            else:
                print('elllllllllllllllllls')
                # No records exist, start numbering from 1
                vals['unique_number'] = '000001'
                result = super(AccountMoveExtended, self).create(vals)

        return result


   
