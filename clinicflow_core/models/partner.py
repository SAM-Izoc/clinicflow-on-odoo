from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_pet_owner = fields.Boolean(string="Is Pet Owner", default=False, help="Check if this contact is a pet owner.")
    pet_ids = fields.One2many('clinicflow.pet', 'owner_id', string="Pets")
