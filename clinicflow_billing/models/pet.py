from odoo import models, fields, api

class ClinicFlowPet(models.Model):
    _inherit = 'clinicflow.pet'

    outstanding_balance = fields.Float(string="Outstanding Balance", compute="_compute_billing_quick_info", store=True)
    invoice_ids = fields.One2many('account.move', 'pet_id', string="Invoices")

    @api.depends('invoice_ids.amount_residual', 'invoice_ids.state', 'invoice_ids.payment_state')
    def _compute_billing_quick_info(self):
        for rec in self:
            posted_invoices = rec.invoice_ids.filtered(lambda i: i.state == 'posted' and i.payment_state not in ['paid', 'in_payment'])
            rec.outstanding_balance = sum(posted_invoices.mapped('amount_residual'))

    def action_view_invoices(self):
        self.ensure_one()
        return {
            'name': f"Invoices - {self.name}",
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('pet_id', '=', self.id)],
            'context': {'default_pet_id': self.id, 'default_move_type': 'out_invoice'},
        }
