from odoo import models, fields, api
from odoo.exceptions import UserError

class ClinicFlowVisit(models.Model):
    _inherit = 'clinicflow.visit'

    ai_audit_id = fields.Many2one(
        'clinicflow.ai.audit', 
        string="AI Audit Log", 
        readonly=True,
        ondelete='set null'
    )
    is_ai_generated = fields.Boolean(string="AI Charted", default=False, readonly=True)
    
    ai_provider = fields.Char(
        related='ai_audit_id.provider', 
        string="AI Provider", 
        readonly=True, 
        store=True
    )
    ai_generated_date = fields.Datetime(
        related='ai_audit_id.generated_at', 
        string="AI Generation Date", 
        readonly=True, 
        store=True
    )
    
    ai_approved_by = fields.Many2one(
        'res.users', 
        string="AI Approved By", 
        help="The clinician who reviewed and approved this AI charting."
    )
    is_ai_edited = fields.Boolean(string="AI Edited", default=False, readonly=True)
    ai_edited_by = fields.Many2one('res.users', string="AI Edited By", readonly=True)

    def write(self, vals):
        """ Tracks changes made to AI-generated SOAP notes to log manual editing history """
        for rec in self:
            if rec.is_ai_generated:
                soap_fields = ['soap_s', 'soap_o', 'soap_a', 'soap_p']
                if any(f in vals for f in soap_fields):
                    vals['is_ai_edited'] = True
                    vals['ai_edited_by'] = self.env.user.id
        return super().write(vals)

    def action_generate_ai_soap(self):
        """ Calls the AI service router to generate contextual SOAP notes """
        self.ensure_one()
        
        # Verify that SOAP fields are empty to prevent overwriting clinician input
        if self.soap_s or self.soap_o or self.soap_a or self.soap_p:
            raise UserError(
                "SOAP charting already contains text. AI generation is disabled to prevent overwriting custom input."
            )
            
        # Build context dict
        context = {
            'visit_id': self.id,
            'pet_name': self.pet_id.name,
            'species': self.pet_id.species or 'dog',
            'breed': self.pet_id.breed or 'Mixed',
            'age': self.pet_id.age_display or 'Unknown',
            'chronic_conditions': self.pet_id.chronic_conditions or 'None',
            'allergies': self.pet_id.allergies or 'None',
            'surgical_history': self.pet_id.surgical_history or 'None',
            'reason_for_visit': self.reason_for_visit or 'Routine checkup',
        }

        # Request generation from AI service
        res = self.env['clinicflow.ai.service'].generate_content('soap', context)
        
        if not res.get('success'):
            raise UserError(f"AI Generation Failed: {res.get('error', 'Unknown Error')}")

        # Update clinical SOAP fields
        self.write({
            'soap_s': res.get('soap_s'),
            'soap_o': res.get('soap_o'),
            'soap_a': res.get('soap_a'),
            'soap_p': res.get('soap_p'),
            'ai_audit_id': res.get('audit_record_id'),
            'is_ai_generated': True,
        })
        
        # Post timeline activity
        self.env['clinicflow.timeline.event'].create({
            'pet_id': self.pet_id.id,
            'event_type': 'visit',
            'event_date': fields.Datetime.now(),
            'name': f"AI Charting Generated (Provider: {res.get('provider_name', 'MOCK')})",
            'res_model': 'clinicflow.visit',
            'res_id': self.id,
        })
        return True
