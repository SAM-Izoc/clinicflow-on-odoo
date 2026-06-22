from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    visit_ids = fields.One2many('clinicflow.visit', 'owner_id', string="Visits")
    appointment_ids = fields.Many2many('calendar.event', string="Appointments", compute="_compute_appointment_ids")

    @api.depends('pet_ids')
    def _compute_appointment_ids(self):
        for partner in self:
            partner.appointment_ids = self.env['calendar.event'].search([('pet_id', 'in', partner.pet_ids.ids)])
