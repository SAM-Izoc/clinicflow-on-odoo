class BaseAIProvider:
    def generate(self, task_type, context, prompt_template):
        """
        Abstract generate method to be overridden by child providers.
        task_type: Selection string ('soap', 'discharge', 'owner_instructions', 'referral', 'summary')
        context: Dict containing variables for rendering the prompt.
        prompt_template: String containing prompt instructions from markdown.
        """
        raise NotImplementedError("Each Swappable AI Provider must implement the 'generate' method.")
