import os
import hashlib
from odoo import models, fields, api

class ClinicFlowAIService(models.AbstractModel):
    _name = 'clinicflow.ai.service'
    _description = 'ClinicFlow AI Provider Service Abstraction'

    @api.model
    def generate_content(self, task_type, context):
        """
        Generic entry point for swappable clinical AI generation.
        task_type: Selection ('soap', 'discharge', 'owner_instructions', 'referral')
        context: Dict containing inputs (e.g. pet_name, chronic_conditions)
        """
        # Load prompt template from prompts/ Markdown folder
        addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        prompt_file = os.path.join(addon_dir, 'prompts', f"{task_type}.md")
        prompt_content = ""
        if os.path.exists(prompt_file):
            try:
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    prompt_content = f.read()
            except Exception:
                pass

        # Load swappable provider class
        provider_type = self.env['ir.config_parameter'].sudo().get_param('clinicflow_ai.provider_type', 'mock')
        
        if provider_type == 'mock':
            from ..providers.mock_provider import MockAIProvider
            provider = MockAIProvider()
        elif provider_type == 'gemini':
            from ..providers.gemini_provider import GeminiProvider
            provider = GeminiProvider()
        elif provider_type == 'claude':
            from ..providers.claude_provider import ClaudeProvider
            provider = ClaudeProvider()
        elif provider_type == 'openai':
            from ..providers.openai_provider import OpenAIProvider
            provider = OpenAIProvider()
        else:
            from ..providers.mock_provider import MockAIProvider
            provider = MockAIProvider()

        # Render prompt templates and generate response
        formatted_prompt = prompt_content.format(**context)
        response = provider.generate(task_type, context, formatted_prompt)

        if not response.get('success'):
            return response

        # Compute prompt/response hashes for audit logs
        p_hash = hashlib.sha256(formatted_prompt.encode('utf-8')).hexdigest()[:16]
        
        # Capture raw text or SOAP segments for hashing
        resp_text = str(response.get('text', ''))
        if task_type == 'soap':
            resp_text = f"{response.get('soap_s')}{response.get('soap_o')}{response.get('soap_a')}{response.get('soap_p')}"
        r_hash = hashlib.sha256(resp_text.encode('utf-8')).hexdigest()[:16]

        # Log AI Audit Trail
        audit_vals = {
            'visit_id': context.get('visit_id'),
            'provider': response.get('provider_name', provider_type.upper()),
            'task_type': task_type,
            'prompt_hash': p_hash,
            'response_hash': r_hash,
            'tokens': response.get('tokens_used', 0),
            'cost': response.get('estimated_cost', 0.0),
        }
        audit_record = self.env['clinicflow.ai.audit'].create(audit_vals)
        
        response['audit_record_id'] = audit_record.id
        return response
