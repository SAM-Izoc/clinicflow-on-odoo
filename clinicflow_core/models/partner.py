from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_pet_owner = fields.Boolean(string="Is Pet Owner", default=False, help="Check if this contact is a pet owner.")
    pet_ids = fields.One2many('clinicflow.pet', 'owner_id', string="Pets")


class ResUsers(models.Model):
    _inherit = 'res.users'

    recent_pet_ids = fields.Many2many(
        'clinicflow.pet', 
        'res_users_recent_pets_rel', 
        'user_id', 
        'pet_id', 
        string="Recent Patients"
    )

    def _add_recent_pet(self, pet):
        """ Appends a pet to the user's recent patients list, keeps it ordered, and caps at 5 records """
        self.ensure_one()
        try:
            # Use sudo() to ensure writing the user relation does not cause access errors for standard users
            current_pets = self.sudo().recent_pet_ids.filtered(lambda p: p.id != pet.id)
            new_pets = pet | current_pets
            self.sudo().write({'recent_pet_ids': [(6, 0, new_pets[:5].ids)]})
        except Exception:
            pass

    def action_view_recent_pets(self):
        """ Returns a list view action containing the current user's recently opened pets """
        self.ensure_one()
        return {
            'name': 'Recent Patients',
            'type': 'ir.actions.act_window',
            'res_model': 'clinicflow.pet',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.recent_pet_ids.ids)],
        }
