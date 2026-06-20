from .base_provider import BaseAIProvider
from .mock_provider import MockAIProvider

class OpenAIProvider(BaseAIProvider):
    def generate(self, task_type, context, prompt_template):
        """ Future integration point for OpenAI API. Falls back to mock for now. """
        mock = MockAIProvider()
        res = mock.generate(task_type, context, prompt_template)
        if res.get('success'):
            res['provider_name'] = 'OpenAI (Mocked)'
        return res
