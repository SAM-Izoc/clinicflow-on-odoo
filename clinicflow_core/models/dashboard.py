from odoo import models, fields, api
import datetime

class ClinicFlowDashboard(models.TransientModel):
    _name = 'clinicflow.dashboard'
    _description = 'ClinicFlow Dashboard Helper'

    reception_today_appointments = fields.Integer(string="Today's Appointments", compute="_compute_metrics")
    reception_waiting = fields.Integer(string="Waiting Queue", compute="_compute_metrics")
    reception_checked_in = fields.Integer(string="Checked In", compute="_compute_metrics")
    reception_billing_pending = fields.Integer(string="Billing Pending Visits", compute="_compute_metrics")
    reception_no_shows = fields.Integer(string="No Shows Today", compute="_compute_metrics")

    vet_today_patients = fields.Integer(string="Today's Patients", compute="_compute_metrics")
    vet_open_consultations = fields.Integer(string="Open SOAP Consultations", compute="_compute_metrics")
    vet_hospitalized = fields.Integer(string="Hospitalized Patients", compute="_compute_metrics")

    mgmt_revenue_today = fields.Float(string="Revenue Today", compute="_compute_metrics")
    mgmt_patients_seen = fields.Integer(string="Patients Seen Today", compute="_compute_metrics")
    mgmt_outstanding_invoices = fields.Float(string="Outstanding Invoices Balance", compute="_compute_metrics")

    def _compute_metrics(self):
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
        billing_visits = self.env['clinicflow.visit'].search([
            ('status', '=', 'billing')
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
        
        invoices_today = self.env['account.move'].search([
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('invoice_date', '=', fields.Date.today())
        ])
        revenue_today = sum(invoices_today.mapped('amount_total'))

        outstanding_invoices = self.env['account.move'].search([
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('payment_state', 'not in', ['paid', 'in_payment'])
        ])
        outstanding_sum = sum(outstanding_invoices.mapped('amount_residual'))

        for rec in self:
            rec.reception_today_appointments = len(appointments)
            rec.reception_waiting = len(waiting_visits)
            rec.reception_checked_in = len(checked_in_visits)
            rec.reception_billing_pending = len(billing_visits)
            rec.reception_no_shows = len(no_shows)

            rec.vet_today_patients = today_patients_count
            rec.vet_open_consultations = len(consultations)
            rec.vet_hospitalized = len(admissions)

            rec.mgmt_revenue_today = revenue_today
            rec.mgmt_patients_seen = len(completed_visits_today)
            rec.mgmt_outstanding_invoices = outstanding_sum

    @api.model
    def action_open_dashboard(self):
        """ Creates a transient dashboard record and returns a form view action for it """
        record = self.create({})
        return {
            'name': 'ClinicFlow Operations Dashboard',
            'type': 'ir.actions.act_window',
            'res_model': 'clinicflow.dashboard',
            'view_mode': 'form',
            'res_id': record.id,
            'target': 'current',
            'context': {'create': False, 'edit': False, 'delete': False},
        }
