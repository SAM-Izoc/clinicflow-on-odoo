from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    outreach_channel_priority = fields.Char(
        string="Outreach Channel Priority",
        config_parameter='clinicflow_outreach.channel_priority',
        default='whatsapp,sms,email',
        help="Comma-separated channel priorities, e.g. 'whatsapp,sms,email'."
    )
    outreach_throttle_days = fields.Integer(
        string="Outreach Throttle Days",
        config_parameter='clinicflow_outreach.throttle_days',
        default=7,
        help="Prevent duplicate reminders within this number of days."
    )
