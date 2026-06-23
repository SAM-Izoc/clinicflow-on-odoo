from odoo import models, fields, api

class ClinicFlowDashboard(models.TransientModel):
    _name = 'clinicflow.dashboard'
    _description = 'ClinicFlow Dashboard Helper'

    name = fields.Char(string="Name", default="ClinicFlow Operations Dashboard")

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
        for rec in self:
            rec.reception_today_appointments = 0
            rec.reception_waiting = 0
            rec.reception_checked_in = 0
            rec.reception_billing_pending = 0
            rec.reception_no_shows = 0

            rec.vet_today_patients = 0
            rec.vet_open_consultations = 0
            rec.vet_hospitalized = 0

            rec.mgmt_revenue_today = 0.0
            rec.mgmt_patients_seen = 0
            rec.mgmt_outstanding_invoices = 0.0

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
