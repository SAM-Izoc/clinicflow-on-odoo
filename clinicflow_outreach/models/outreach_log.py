from odoo import models, fields

class ClinicFlowOutreachLog(models.Model):
    _name = 'clinicflow.outreach.log'
    _description = 'Outreach Message Log'
    _order = 'create_date desc'

    partner_id = fields.Many2one('res.partner', string="Owner", required=True, index=True)
    pet_id = fields.Many2one('clinicflow.pet', string="Pet Patient", required=True, index=True)
    vaccination_id = fields.Many2one('clinicflow.vaccination', string="Vaccination Record", index=True)
    channel = fields.Selection([
        ('whatsapp', 'WhatsApp'),
        ('sms', 'SMS'),
        ('email', 'Email'),
    ], string="Channel", required=True)
    recipient = fields.Char(string="Recipient Details", required=True)
    message_body = fields.Text(string="Compiled Message", required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('queued', 'Queued'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ], string="Status", default='draft', required=True, index=True)
    error_message = fields.Text(string="Error Message")
    date_sent = fields.Datetime(string="Date Sent")
