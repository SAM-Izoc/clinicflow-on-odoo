from odoo import models, fields, api

class ClinicFlowPet(models.Model):
    _inherit = 'clinicflow.pet'

    # Stored computed search metrics (Clinical)
    last_visit_date = fields.Date(string="Last Visit", compute="_compute_clinical_quick_info", store=True)
    upcoming_appointment_date = fields.Datetime(string="Upcoming Appointment", compute="_compute_clinical_quick_info", store=True)

    # Relations
    visit_ids = fields.One2many('clinicflow.visit', 'pet_id', string="Visits")
    vaccination_ids = fields.One2many('clinicflow.vaccination', 'pet_id', string="Vaccinations")
    prescription_ids = fields.One2many('clinicflow.prescription', 'pet_id', string="Prescriptions")
    admission_ids = fields.One2many('clinicflow.admission', 'pet_id', string="Hospitalizations")
    timeline_ids = fields.One2many('clinicflow.timeline.event', 'pet_id', string="Timeline Events")
    appointment_ids = fields.One2many('calendar.event', 'pet_id', string="Appointments")

    @api.depends('visit_ids.date', 'visit_ids.status',
                 'appointment_ids.start', 'appointment_ids.pet_id')
    def _compute_clinical_quick_info(self):
        today = fields.Datetime.now()
        for rec in self:
            # 1. Stored Last Visit Date
            completed_visits = rec.visit_ids.filtered(lambda v: v.status == 'completed' and v.date)
            if completed_visits:
                rec.last_visit_date = completed_visits.sorted('date', reverse=True)[0].date.date()
            else:
                rec.last_visit_date = False

            # 2. Stored Upcoming Appointment Date
            future_events = rec.appointment_ids.filtered(lambda e: e.start and e.start > today)
            if future_events:
                rec.upcoming_appointment_date = future_events.sorted('start')[0].start
            else:
                rec.upcoming_appointment_date = False

    # Quick action header helpers
    def action_create_appointment_quick(self):
        self.ensure_one()
        return {
            'name': 'New Appointment',
            'type': 'ir.actions.act_window',
            'res_model': 'calendar.event',
            'view_mode': 'form',
            'context': {
                'default_pet_id': self.id,
                'default_name': f"Consultation: {self.name}",
                'default_partner_ids': [self.owner_id.id] if self.owner_id else [],
            },
            'target': 'new',
        }

    def action_create_visit_quick(self):
        self.ensure_one()
        return {
            'name': 'New Visit SOAP',
            'type': 'ir.actions.act_window',
            'res_model': 'clinicflow.visit',
            'view_mode': 'form',
            'context': {
                'default_pet_id': self.id,
                'default_status': 'consultation',
            },
        }

    def action_create_prescription_quick(self):
        self.ensure_one()
        active_visit = self.env['clinicflow.visit'].search([
            ('pet_id', '=', self.id), 
            ('status', 'not in', ['completed', 'booked'])
        ], limit=1)
        return {
            'name': 'New Prescription',
            'type': 'ir.actions.act_window',
            'res_model': 'clinicflow.prescription',
            'view_mode': 'form',
            'context': {
                'default_pet_id': self.id,
                'default_visit_id': active_visit.id if active_visit else False,
            },
            'target': 'new',
        }

    def action_create_vaccination_quick(self):
        self.ensure_one()
        return {
            'name': 'New Vaccination',
            'type': 'ir.actions.act_window',
            'res_model': 'clinicflow.vaccination',
            'view_mode': 'form',
            'context': {
                'default_pet_id': self.id,
            },
            'target': 'new',
        }

    def action_create_admission_quick(self):
        self.ensure_one()
        active_visit = self.env['clinicflow.visit'].search([
            ('pet_id', '=', self.id), 
            ('status', 'not in', ['completed', 'booked'])
        ], limit=1)
        return {
            'name': 'New Hospitalization',
            'type': 'ir.actions.act_window',
            'res_model': 'clinicflow.admission',
            'view_mode': 'form',
            'context': {
                'default_pet_id': self.id,
                'default_visit_id': active_visit.id if active_visit else False,
            },
            'target': 'new',
        }
