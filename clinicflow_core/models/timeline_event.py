from odoo import models, fields

class ClinicFlowTimelineEvent(models.Model):
    _name = 'clinicflow.timeline.event'
    _description = 'Patient Activity Timeline Event'
    _order = 'event_date desc, id desc'

    pet_id = fields.Many2one('clinicflow.pet', string="Pet Patient", required=True, ondelete='cascade', index=True)
    event_type = fields.Selection([
        ('visit', 'Clinic Visit'),
        ('vaccination', 'Vaccination'),
        ('prescription', 'Prescription'),
        ('invoice', 'Billing Invoice'),
        ('admission', 'Hospital Admission')
    ], string="Event Type", required=True)
    event_date = fields.Datetime(string="Event Date", default=fields.Datetime.now, required=True)
    name = fields.Char(string="Event Title", required=True)
    res_model = fields.Char(string="Target Model")
    res_id = fields.Integer(string="Target Record ID")
