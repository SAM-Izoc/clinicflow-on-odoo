from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    pet_id = fields.Many2one('clinicflow.pet', string="Pet Patient", index=True, help="Links invoice to the specific pet patient.")
