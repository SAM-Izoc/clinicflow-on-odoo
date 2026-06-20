from odoo import models, fields, api
import datetime

class ClinicFlowDashboard(models.TransientModel):
    _inherit = 'clinicflow.dashboard'

    def _compute_metrics(self):
        super()._compute_metrics()
        today_start = datetime.datetime.combine(fields.Date.today(), datetime.time.min)
        today_end = datetime.datetime.combine(fields.Date.today(), datetime.time.max)

        # 1. Appointments starting today
        appointments = self.env['calendar.event'].search([
            ('start', '>=', today_start),
            ('start', '<=', today_end)
        ])
        no_shows = self.env['calendar.event'].search([
            ('appointment_status', '=', 'no_show'),
            ('start', '>=', today_start),
            ('start', '<=', today_end)
        ])
        
        # 2. Visits statuses
        waiting_visits = self.env['clinicflow.visit'].search([
            ('status', '=', 'waiting'), 
            ('date', '>=', today_start), 
            ('date', '<=', today_end)
        ])
        checked_in_visits = self.env['clinicflow.visit'].search([
            ('status', '=', 'check_in'), 
            ('date', '>=', today_start), 
            ('date', '<=', today_end)
        ])

        # 3. Vet metrics
        consultations = self.env['clinicflow.visit'].search([
            ('status', '=', 'consultation')
        ])
        admissions = self.env['clinicflow.admission'].search([
            ('state', '=', 'admitted')
        ])
        
        active_patient_visits = self.env['clinicflow.visit'].search([
            ('status', 'in', ['consultation', 'treatment']),
            ('date', '>=', today_start),
            ('date', '<=', today_end)
        ])
        today_patients_count = len(active_patient_visits.mapped('pet_id'))

        # 4. Mgmt metrics
        completed_visits_today = self.env['clinicflow.visit'].search([
            ('status', '=', 'completed'),
            ('date', '>=', today_start),
            ('date', '<=', today_end)
        ])

        for rec in self:
            rec.reception_today_appointments = len(appointments)
            rec.reception_waiting = len(waiting_visits)
            rec.reception_checked_in = len(checked_in_visits)
            rec.reception_no_shows = len(no_shows)

            rec.vet_today_patients = today_patients_count
            rec.vet_open_consultations = len(consultations)
            rec.vet_hospitalized = len(admissions)
            rec.mgmt_patients_seen = len(completed_visits_today)
