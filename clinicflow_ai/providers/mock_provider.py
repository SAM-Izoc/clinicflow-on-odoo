from .base_provider import BaseAIProvider

class MockAIProvider(BaseAIProvider):
    def generate(self, task_type, context, prompt_template):
        """ Local template simulation returning contextual data based on symptoms """
        pet_name = context.get('pet_name', 'Patient')
        species = context.get('species', 'dog')
        breed = context.get('breed', 'Mixed')
        age = context.get('age', 'Unknown')
        reason = context.get('reason_for_visit', 'Routine wellness check')
        chronic = context.get('chronic_conditions', 'None')
        allergies = context.get('allergies', 'None')

        if task_type == 'soap':
            reason_lower = reason.lower()
            if 'limping' in reason_lower or 'lame' in reason_lower or 'leg' in reason_lower:
                s = f"Owner reports {pet_name} has been limping on the hind left leg after moderate exercise. Chronics: {chronic}."
                o = f"Limping observed on hind left leg. Mild pain and sensitivity on extension of left stifle/hip joint. No swelling or heat detected. Weight and vitals normal."
                a = f"Suspected arthritis flare-up or ligament strain. History of {chronic}."
                p = f"Prescribe Carprofen 75mg twice daily with food for 7 days. Recommend strict cage rest and joint supplements. Recheck in 7 days."
            elif 'cough' in reason_lower or 'respiratory' in reason_lower:
                s = f"Owner reports {pet_name} has a dry honking cough for 3 days, especially when excited. Allergies: {allergies}."
                o = f"Tracheal pinch positive. Heart sounds clear, no murmur. Lungs clear on auscultation. Temperature 38.9C."
                a = f"Suspected infectious tracheobronchitis (Kennel Cough)."
                p = f"Prescribe Temaril-P twice daily for 5 days. Restrict exercise. Keep isolated from other dogs for 10 days."
            elif 'vomit' in reason_lower or 'diarrhea' in reason_lower or 'stomach' in reason_lower:
                s = f"Owner reports 3 episodes of vomiting over past 24 hours. Decreased appetite but drinking water."
                o = f"Abdomen soft, non-painful. Hydration normal. Mucous membranes pink and moist. Temp 38.5C."
                a = f"Acute gastroenteritis, suspected dietary indiscretion."
                p = f"Fasting for 12 hours, then introduction of bland diet (boiled chicken & rice). Prescribe Cerenia 10mg once daily for 3 days."
            else:
                s = f"{pet_name} presented for routine wellness exam. Owner reports active, eating well, normal stools."
                o = f"A&R, clear eyes, ears clean, teeth show mild tartar. Heart and lungs clear. Body condition score 5/9."
                a = f"Healthy {species} ({breed}), age {age}."
                p = f"Administer due vaccinations. Continue monthly flea/tick preventative. Recheck weight in 1 year."

            return {
                'success': True,
                'soap_s': s,
                'soap_o': o,
                'soap_a': a,
                'soap_p': p,
                'tokens_used': 350,
                'estimated_cost': 0.0007,
            }
        elif task_type == 'discharge':
            return {
                'success': True,
                'text': f"Discharge instructions for {pet_name}:\n- Limit activity for next 24-48 hours.\n- Administer medications as prescribed.\n- Monitor incision or symptoms carefully.\n- Call the clinic immediately if lethargy or vomiting occurs.",
                'tokens_used': 150,
                'estimated_cost': 0.0003,
            }
        elif task_type == 'owner_instructions':
            return {
                'success': True,
                'text': f"Care Guide for {pet_name} ({species}):\n- Keep active, feed a balanced diet.\n- Watch out for chronic condition flare-ups ({chronic}).\n- Avoid known allergens ({allergies}).",
                'tokens_used': 120,
                'estimated_cost': 0.0002,
            }
        return {
            'success': False,
            'error': 'Unsupported task type'
        }
