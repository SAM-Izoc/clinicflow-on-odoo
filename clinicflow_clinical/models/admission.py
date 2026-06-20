from odoo import models, fields, api

class ClinicFlowAdmission(models.Model):
    _name = 'clinicflow.admission'
    _description = 'Veterinary Hospitalization Admission'
    _order = 'admission_date desc'

    name = fields.Char(string="Admission ID", required=True, copy=False, readonly=True, default='New')
    pet_id = fields.Many2one('clinicflow.pet', string="Pet Patient", required=True)
    owner_id = fields.Many2one(related='pet_id.owner_id', string="Owner", readonly=True, store=True)
    visit_id = fields.Many2one('clinicflow.visit', string="Originating Visit")
    admission_date = fields.Datetime(string="Admission Date", default=fields.Datetime.now, required=True)
    discharge_date = fields.Datetime(string="Discharge Date")
    reason = fields.Text(string="Reason for Admission")
    state = fields.Selection([
        ('admitted', 'Admitted'),
        ('discharged', 'Discharged')
    ], string="Status", default='admitted', required=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                today = fields.Datetime.now()
                vals['name'] = f"ADM-{today.strftime('%Y%m%d%H%M%S')}"
        records = super().create(vals_list)
        for rec in records:
            self.env['clinicflow.timeline.event'].create({
                'pet_id': rec.pet_id.id,
                'event_type': 'admission',
                'event_date': rec.admission_date,
                'name': f"Hospitalization Admitted: {rec.name} (Reason: {rec.reason or 'Surgical observation'})",
                'res_model': 'clinicflow.admission',
                'res_id': rec.id
            })
        return records
