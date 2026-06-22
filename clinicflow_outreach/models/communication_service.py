import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class ClinicFlowCommunicationService(models.AbstractModel):
    _name = 'clinicflow.communication.service'
    _description = 'Decoupled Communication Service Abstraction'

    @api.model
    def send_message(self, log):
        """ Primary gateway to send outreach logs through the appropriate provider channel """
        if not log:
            return False

        log.write({'state': 'queued'})
        
        success = False
        error_msg = ""

        try:
            if log.channel == 'whatsapp':
                success, error_msg = self._send_whatsapp(log)
            elif log.channel == 'sms':
                success, error_msg = self._send_sms(log)
            elif log.channel == 'email':
                success, error_msg = self._send_email(log)
            else:
                success, error_msg = False, f"Unsupported channel: {log.channel}"
        except Exception as e:
            success = False
            error_msg = str(e)

        if success:
            log.write({
                'state': 'sent',
                'date_sent': fields.Datetime.now(),
                'error_message': False,
            })
            _logger.info("Outreach reminder successfully sent to %s via %s (Log ID: %s)", log.recipient, log.channel, log.id)
            return True
        else:
            log.write({
                'state': 'failed',
                'error_message': error_msg,
            })
            _logger.error("Outreach reminder failed for %s via %s: %s (Log ID: %s)", log.recipient, log.channel, error_msg, log.id)
            return False

    @api.model
    def _send_whatsapp(self, log):
        """ Mock WhatsApp Provider integration. Logs payload to server console. """
        _logger.info("\n=== MOCK WHATSAPP OUTGOING REMINDER ===\nTo: %s\nMessage: %s\n=====================================", log.recipient, log.message_body)
        return True, ""

    @api.model
    def _send_sms(self, log):
        """ Mock SMS Provider (e.g. Twilio) integration. Logs payload to server console. """
        _logger.info("\n=== MOCK SMS OUTGOING REMINDER ===\nTo: %s\nMessage: %s\n=====================================", log.recipient, log.message_body)
        return True, ""

    @api.model
    def _send_email(self, log):
        """ Mock Email integration. In the future, this can invoke Odoo's native mail.mail gateway """
        _logger.info("\n=== MOCK EMAIL OUTGOING REMINDER ===\nTo: %s\nSubject: %s\nBody: %s\n=====================================", log.recipient, "Vaccination Reminder: " + (log.vaccination_id.vaccine_product_id.name or "Upcoming Vaccine"), log.message_body)
        return True, ""
