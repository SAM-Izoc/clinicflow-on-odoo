from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    total_outstanding_balance = fields.Float(
        string="Total Outstanding Balance",
        compute="_compute_total_outstanding_balance",
        store=True
    )

    @api.depends('pet_ids.outstanding_balance')
    def _compute_total_outstanding_balance(self):
        for partner in self:
            partner.total_outstanding_balance = sum(partner.pet_ids.mapped('outstanding_balance'))

    def action_view_outstanding_invoices(self):
        self.ensure_one()
        return {
            'name': f"Outstanding Invoices - {self.name}",
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [
                ('partner_id', '=', self.id),
                ('state', '=', 'posted'),
                ('payment_state', 'not in', ['paid', 'in_payment'])
            ],
            'context': {'default_partner_id': self.id, 'default_move_type': 'out_invoice'},
        }
