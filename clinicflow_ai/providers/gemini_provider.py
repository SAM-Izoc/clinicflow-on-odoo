from .base_provider import BaseAIProvider
from .mock_provider import MockAIProvider

class GeminiProvider(BaseAIProvider):
    def generate(self, task_type, context, prompt_template):
        """ Future integration point for Google Gemini API. Falls back to mock for now. """
        # TODO: Implement actual Gemini API call (e.g. using google-generativeai package)
        mock = MockAIProvider()
        res = mock.generate(task_type, context, prompt_template)
        if res.get('success'):
            res['provider_name'] = 'Google Gemini (Mocked)'
        return res
