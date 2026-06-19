from odoo import models, fields, api

class ClinicFlowVaccination(models.Model):
    _name = 'clinicflow.vaccination'
    _description = 'Veterinary Vaccination Record'
    _order = 'date_administered desc'

    pet_id = fields.Many2one('clinicflow.pet', string="Pet Patient", required=True)
    owner_id = fields.Many2one(related='pet_id.owner_id', string="Owner", readonly=True, store=True)
    vaccine_product_id = fields.Many2one(
        'product.product', 
        string="Vaccine Product", 
        domain="[('type', 'in', ['consu', 'product'])]", 
        required=True,
        help="Links directly to Odoo products for inventory mapping."
    )
    date_administered = fields.Date(string="Date Administered", default=fields.Date.today, required=True)
    date_due = fields.Date(string="Date Due")
    status = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('administered', 'Administered'),
        ('overdue', 'Overdue')
    ], string="Status", default='administered', required=True)
    remarks = fields.Text(string="Remarks")

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            event_datetime = fields.Datetime.now()
            if rec.date_administered:
                event_datetime = fields.Datetime.to_datetime(rec.date_administered)
            self.env['clinicflow.timeline.event'].create({
                'pet_id': rec.pet_id.id,
                'event_type': 'vaccination',
                'event_date': event_datetime,
                'name': f"Vaccine Administered: {rec.vaccine_product_id.name}",
                'res_model': 'clinicflow.vaccination',
                'res_id': rec.id
            })
        return records

