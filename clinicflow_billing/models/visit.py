from odoo import models, fields, api

class ClinicFlowVisit(models.Model):
    _inherit = 'clinicflow.visit'

    def action_create_invoice(self):
        invoice = super().action_create_invoice()
        if invoice and self.pet_id:
            invoice.write({'pet_id': self.pet_id.id})
        return invoice
