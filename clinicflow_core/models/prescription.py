from odoo import models, fields, api

class ClinicFlowPrescription(models.Model):
    _name = 'clinicflow.prescription'
    _description = 'Veterinary Prescription'
    _order = 'date desc'

    name = fields.Char(string="Prescription ID", required=True, copy=False, readonly=True, default='New')
    pet_id = fields.Many2one('clinicflow.pet', string="Pet Patient", required=True)
    visit_id = fields.Many2one('clinicflow.visit', string="Visit", required=True)
    owner_id = fields.Many2one(related='pet_id.owner_id', string="Owner", readonly=True, store=True)
    date = fields.Date(string="Prescription Date", default=fields.Date.today, required=True)
    line_ids = fields.One2many('clinicflow.prescription.line', 'prescription_id', string="Prescription Lines")
    notes = fields.Text(string="General Instructions")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                today = fields.Datetime.now()
                vals['name'] = f"PR-{today.strftime('%Y%m%d%H%M%S')}"
        records = super().create(vals_list)
        for rec in records:
            self.env['clinicflow.timeline.event'].create({
                'pet_id': rec.pet_id.id,
                'event_type': 'prescription',
                'event_date': fields.Datetime.now(),
                'name': f"Prescription Issued: {rec.name}",
                'res_model': 'clinicflow.prescription',
                'res_id': rec.id
            })
        return records


class ClinicFlowPrescriptionLine(models.Model):
    _name = 'clinicflow.prescription.line'
    _description = 'Prescription Line'

    prescription_id = fields.Many2one('clinicflow.prescription', string="Prescription", required=True, ondelete='cascade')
    product_id = fields.Many2one(
        'product.product', 
        string="Medication (Product)", 
        required=True,
        domain="[('type', 'in', ['consu', 'product'])]",
        help="Links directly to Odoo core product inventory."
    )
    quantity = fields.Float(string="Quantity", default=1.0, required=True)
    dosage = fields.Selection([
        ('1-0-0', 'Morning Only'),
        ('0-1-0', 'Afternoon Only'),
        ('0-0-1', 'Night Only'),
        ('1-0-1', 'Morning and Night'),
        ('1-1-1', 'Thrice a day')
    ], string="Dosage Frequency", default='1-0-0')
    instructions = fields.Text(string="Usage Instructions")
