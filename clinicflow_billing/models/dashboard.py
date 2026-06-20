from odoo import models, fields, api
import datetime

class ClinicFlowDashboard(models.TransientModel):
    _inherit = 'clinicflow.dashboard'

    def _compute_metrics(self):
        super()._compute_metrics()
        
        billing_visits = self.env['clinicflow.visit'].search([
            ('status', '=', 'billing')
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
            rec.reception_billing_pending = len(billing_visits)
            rec.mgmt_revenue_today = revenue_today
            rec.mgmt_outstanding_invoices = outstanding_sum
