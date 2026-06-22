from odoo import models, fields

class ClinicFlowOutreachTemplate(models.Model):
    _name = 'clinicflow.outreach.template'
    _description = 'Outreach Reminder Template'

    name = fields.Char(string="Template Name", required=True)
    channel = fields.Selection([
        ('whatsapp', 'WhatsApp'),
        ('sms', 'SMS'),
        ('email', 'Email'),
    ], string="Channel", required=True, default='whatsapp')
    subject = fields.Char(string="Subject", help="Subject line for emails.")
    body = fields.Text(string="Body Content", required=True, help="Use {{owner_name}}, {{pet_name}}, {{vaccine_name}}, {{due_date}} as placeholders.")
