from odoo import models, fields

class ClinicFlowWeightRecord(models.Model):
    _name = 'clinicflow.weight.record'
    _description = 'Patient Weight Record'
    _order = 'date desc, id desc'

    pet_id = fields.Many2one('clinicflow.pet', string="Pet Patient", required=True, ondelete='cascade', index=True)
    weight = fields.Float(string="Weight (kg)", required=True)
    date = fields.Date(string="Date", default=fields.Date.today, required=True)
    notes = fields.Char(string="Notes")
