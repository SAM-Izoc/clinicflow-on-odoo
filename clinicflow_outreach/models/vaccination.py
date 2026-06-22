import datetime
from odoo import models, fields, api
from odoo.exceptions import UserError

class ClinicFlowVaccination(models.Model):
    _inherit = 'clinicflow.vaccination'

    def action_send_reminder(self):
        """ Manual action to compile and send a reminder instantly, bypassing throttle limits """
        self.ensure_one()
        log = self._create_outreach_reminder(force=True)
        if not log:
            raise UserError("Could not generate reminder. Please ensure the pet owner has a phone or email.")
        
        self.env['clinicflow.communication.service'].send_message(log)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Reminder Sent',
                'message': f"Outreach reminder compiled and sent to {log.recipient} via {log.channel}.",
                'type': 'success',
                'sticky': False,
            }
        }

    def _create_outreach_reminder(self, force=False):
        """ Internal method to compile template and create outreach log. Returns the log record or False. """
        self.ensure_one()
        owner = self.pet_id.owner_id
        if not owner:
            return False

        # Load configurations
        config_env = self.env['ir.config_parameter'].sudo()
        throttle_days = int(config_env.get_param('clinicflow_outreach.throttle_days', 7))
        priority_string = config_env.get_param('clinicflow_outreach.channel_priority', 'whatsapp,sms,email')
        priority_channels = [c.strip() for c in priority_string.split(',') if c.strip()]

        # Throttling check (skip if not forced/manual)
        if not force:
            limit_date = fields.Datetime.now() - datetime.timedelta(days=throttle_days)
            existing_log = self.env['clinicflow.outreach.log'].search([
                ('vaccination_id', '=', self.id),
                ('state', 'in', ['queued', 'sent']),
                ('create_date', '>=', limit_date)
            ], limit=1)
            if existing_log:
                # Recently sent, throttle it
                return False

        # Determine best channel and recipient
        selected_channel = False
        recipient = False

        for channel in priority_channels:
            if channel == 'whatsapp' and (owner.mobile or owner.phone):
                selected_channel = 'whatsapp'
                recipient = owner.mobile or owner.phone
                break
            elif channel == 'sms' and (owner.mobile or owner.phone):
                selected_channel = 'sms'
                recipient = owner.mobile or owner.phone
                break
            elif channel == 'email' and owner.email:
                selected_channel = 'email'
                recipient = owner.email
                break

        if not selected_channel or not recipient:
            return False

        # Load template
        template = self.env['clinicflow.outreach.template'].search([('channel', '=', selected_channel)], limit=1)
        
        # Standard fallback template if none exists in database
        if template:
            body = template.body
        else:
            if selected_channel == 'whatsapp':
                body = "Hi {{owner_name}}, this is a reminder that {{pet_name}} is due for their {{vaccine_name}} on {{due_date}}. Please contact us to schedule an appointment."
            elif selected_channel == 'sms':
                body = "Reminder: {{pet_name}} is due for {{vaccine_name}} on {{due_date}}."
            else:
                body = "Dear {{owner_name}},\n\nThis is to remind you that {{pet_name}} is scheduled to receive their {{vaccine_name}} vaccine on {{due_date}}.\n\nBest regards,\n{{clinic_name}}"

        # Resolve placeholders
        owner_name = owner.name or "Client"
        pet_name = self.pet_id.name or "your pet"
        vaccine_name = self.vaccine_product_id.name or "vaccination"
        due_date = fields.Date.to_string(self.date_due) if self.date_due else "soon"
        clinic_name = self.env.company.name or "Your Veterinary Clinic"

        compiled_body = body.replace('{{owner_name}}', owner_name)\
                             .replace('{{pet_name}}', pet_name)\
                             .replace('{{vaccine_name}}', vaccine_name)\
                             .replace('{{due_date}}', due_date)\
                             .replace('{{clinic_name}}', clinic_name)

        # Create log record
        log = self.env['clinicflow.outreach.log'].create({
            'partner_id': owner.id,
            'pet_id': self.pet_id.id,
            'vaccination_id': self.id,
            'channel': selected_channel,
            'recipient': recipient,
            'message_body': compiled_body,
            'state': 'draft',
        })
        return log

    @api.model
    def cron_process_vaccination_reminders(self):
        """ Cron action that executes daily to process reminders for scheduled upcoming or overdue vaccinations """
        # Get target dates: due in next 7 days, or overdue (not administered yet)
        target_date = fields.Date.today() + datetime.timedelta(days=7)
        due_vaccinations = self.search([
            ('status', 'in', ['scheduled', 'overdue']),
            ('date_due', '<=', target_date)
        ])

        processed_count = 0
        for vacc in due_vaccinations:
            log = vacc._create_outreach_reminder(force=False)
            if log:
                self.env['clinicflow.communication.service'].send_message(log)
                processed_count += 1

        return processed_count
