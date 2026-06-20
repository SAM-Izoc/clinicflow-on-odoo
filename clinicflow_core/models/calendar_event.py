from odoo import models, fields, api
from odoo.exceptions import UserError

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    pet_id = fields.Many2one(
        'clinicflow.pet', 
        string="Pet Patient", 
        index=True, 
        help="Links this appointment to a specific pet patient."
    )
    visit_id = fields.Many2one(
        'clinicflow.visit', 
        string="Linked Visit", 
        readonly=True, 
        index=True, 
        help="Visit generated from this appointment."
    )
    appointment_status = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('no_show', 'No Show'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string="Appointment Status", default='scheduled', required=True)

    @api.model_create_multi
    def create(self, vals_list):
        events = super().create(vals_list)
        events.mapped('pet_id').modified(['upcoming_appointment_date'])
        return events

    def write(self, vals):
        old_pets = self.mapped('pet_id')
        res = super().write(vals)
        if 'start' in vals or 'pet_id' in vals or 'active' in vals or 'appointment_status' in vals:
            (old_pets | self.mapped('pet_id')).modified(['upcoming_appointment_date'])
        return res

    def unlink(self):
        pets = self.mapped('pet_id')
        res = super().unlink()
        pets.modified(['upcoming_appointment_date'])
        return res

    def action_check_in_pet(self):
        """ Checks in the pet from the calendar appointment by creating a ClinicFlow Visit """
        self.ensure_one()
        if not self.pet_id:
            raise UserError("Please select a Pet Patient before checking in.")
        
        if self.visit_id:
            # If visit already exists, just open it
            return {
                'name': 'Linked Visit',
                'type': 'ir.actions.act_window',
                'res_model': 'clinicflow.visit',
                'view_mode': 'form',
                'res_id': self.visit_id.id,
                'target': 'current',
            }

        # Create visit
        visit_vals = {
            'pet_id': self.pet_id.id,
            'vet_id': self.user_id.id or self.env.user.id,
            'date': self.start,
            'status': 'check_in',  # checked in stage
            'event_id': self.id,
        }
        
        visit = self.env['clinicflow.visit'].create(visit_vals)
        
        # Link back and update status
        self.write({
            'visit_id': visit.id,
            'appointment_status': 'checked_in'
        })

        # Return action to open the newly created visit form
        return {
            'name': 'Visit Consultation',
            'type': 'ir.actions.act_window',
            'res_model': 'clinicflow.visit',
            'view_mode': 'form',
            'res_id': visit.id,
            'target': 'current',
        }
