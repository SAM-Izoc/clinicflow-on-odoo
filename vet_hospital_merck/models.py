from odoo import models, fields, api
import urllib.parse


class MerckIntegration(models.AbstractModel):
    _name = 'merck.mixin'
    _description = 'Merck Vet Manual Integration Mixin'

    # Configuration field
    merck_base_url = fields.Char(
        string='Merck Base URL',
        default='https://www.msdvetmanual.com/search',
        readonly=True
    )

    def action_search_merck_diagnosis(self):
        """Search diagnosis in Merck Vet Manual"""
        if hasattr(self, 'primary_diagnosis_id') and self.primary_diagnosis_id:
            search_term = self.primary_diagnosis_id.name
            self._open_merck_search(search_term)
        elif hasattr(self, 'name') and self.name:
            self._open_merck_search(self.name)

    def action_search_merck_symptom(self):
        """Search symptoms in Merck Vet Manual"""
        if hasattr(self, 'symptoms') and self.symptoms:
            self._open_merck_search(self.symptoms)
        elif hasattr(self, 'subjective') and self.subjective:
            # Extract first line of subjective
            first_line = self.subjective.split('\n')[0]
            self._open_merck_search(first_line)

    def action_search_merck_condition(self):
        """Search medical condition in Merck Vet Manual"""
        if hasattr(self, 'medical_conditions') and self.medical_conditions:
            first_condition = self.medical_conditions.split(',')[0].strip()
            self._open_merck_search(first_condition)
        elif hasattr(self, 'assessment') and self.assessment:
            first_line = self.assessment.split('\n')[0]
            self._open_merck_search(first_line)

    def action_search_merck_custom(self):
        """Open Merck with custom search"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Search Merck Vet Manual',
                'message': 'Opening Merck Vet Manual...',
                'type': 'success',
                'sticky': False,
            },
        }

    def _open_merck_search(self, search_term):
        """Open Merck Vet Manual with search term"""
        if not search_term:
            return

        # URL encode the search term
        encoded_search = urllib.parse.quote(search_term)
        
        # Merck Vet Manual search URL format
        merck_search_url = f"https://www.msdvetmanual.com/search?query={encoded_search}"
        
        # Return action to open URL in new tab
        return {
            'type': 'ir.actions.act_url',
            'url': merck_search_url,
            'target': 'new',
        }


# Extend Medical Record Model
class MedicalRecordMerck(models.Model):
    _inherit = 'vet.medical_record'

    def action_search_merck_diagnosis(self):
        """Search diagnosis in Merck Vet Manual"""
        if self.primary_diagnosis_id:
            return self._open_merck_search(self.primary_diagnosis_id.name)

    def action_search_merck_symptom(self):
        """Search symptoms in Merck Vet Manual"""
        if self.subjective:
            first_line = self.subjective.split('\n')[0] if self.subjective else "symptoms"
            return self._open_merck_search(first_line)

    def action_search_merck_treatment(self):
        """Search treatment in Merck Vet Manual"""
        if self.plan:
            first_line = self.plan.split('\n')[0] if self.plan else "treatment"
            return self._open_merck_search(first_line)

    def action_search_merck_assessment(self):
        """Search assessment/diagnosis in Merck Vet Manual"""
        if self.assessment:
            first_line = self.assessment.split('\n')[0] if self.assessment else "assessment"
            return self._open_merck_search(first_line)

    def _open_merck_search(self, search_term):
        """Open Merck Vet Manual with search term"""
        import urllib.parse
        
        if not search_term:
            search_term = "veterinary medicine"
        
        # Clean up search term
        search_term = search_term.strip()[:100]  # Limit to 100 chars
        
        # URL encode the search term
        encoded_search = urllib.parse.quote(search_term)
        
        # Merck Vet Manual search URL
        merck_url = f"https://www.msdvetmanual.com/search?query={encoded_search}"
        
        # Open in new tab
        return {
            'type': 'ir.actions.act_url',
            'url': merck_url,
            'target': 'new',
        }


# Extend Patient Model
class PatientMerck(models.Model):
    _inherit = 'vet.patient'

    def action_search_merck_condition(self):
        """Search patient's medical conditions in Merck"""
        if self.medical_conditions:
            first_condition = self.medical_conditions.split(',')[0].strip()
            return self._search_merck(first_condition)
        return self._search_merck(f"{self.species_id.name} health")

    def action_search_merck_breed(self):
        """Search breed-specific information in Merck"""
        search_term = f"{self.breed_id.name if self.breed_id else self.species_id.name} health"
        return self._search_merck(search_term)

    def _search_merck(self, search_term):
        """Open Merck search"""
        import urllib.parse
        
        search_term = search_term.strip()[:100]
        encoded_search = urllib.parse.quote(search_term)
        merck_url = f"https://www.msdvetmanual.com/search?query={encoded_search}"
        
        return {
            'type': 'ir.actions.act_url',
            'url': merck_url,
            'target': 'new',
        }


# Extend Diagnosis Model
class DiagnosisMerck(models.Model):
    _inherit = 'vet.diagnosis'

    def action_search_merck(self):
        """Search diagnosis in Merck Vet Manual"""
        import urllib.parse
        
        search_term = self.name.strip()[:100]
        encoded_search = urllib.parse.quote(search_term)
        merck_url = f"https://www.msdvetmanual.com/search?query={encoded_search}"
        
        return {
            'type': 'ir.actions.act_url',
            'url': merck_url,
            'target': 'new',
        }


# Extend Vital Sign Model
class VitalSignMerck(models.Model):
    _inherit = 'vet.vital_sign'

    def action_search_merck_abnormality(self):
        """Search abnormality in Merck"""
        import urllib.parse
        
        if self.abnormalities:
            search_term = self.abnormalities.split('\n')[0].strip()[:100]
        else:
            alerts = self.get_abnormality_alert()
            search_term = alerts[0] if alerts else "vital signs abnormality"
        
        encoded_search = urllib.parse.quote(search_term)
        merck_url = f"https://www.msdvetmanual.com/search?query={encoded_search}"
        
        return {
            'type': 'ir.actions.act_url',
            'url': merck_url,
            'target': 'new',
        }


# Extend Prescription Model
class PrescriptionMerck(models.Model):
    _inherit = 'vet.prescription'

    def action_search_merck_drug(self):
        """Search drug in Merck Vet Manual"""
        import urllib.parse
        
        search_term = self.medication_name.strip()[:100] if self.medication_name else "medication"
        encoded_search = urllib.parse.quote(search_term)
        merck_url = f"https://www.msdvetmanual.com/search?query={encoded_search}"
        
        return {
            'type': 'ir.actions.act_url',
            'url': merck_url,
            'target': 'new',
        }

    def action_search_merck_indication(self):
        """Search indication/use in Merck"""
        import urllib.parse
        
        search_term = self.instructions.split('\n')[0].strip()[:100] if self.instructions else "drug indication"
        encoded_search = urllib.parse.quote(search_term)
        merck_url = f"https://www.msdvetmanual.com/search?query={encoded_search}"
        
        return {
            'type': 'ir.actions.act_url',
            'url': merck_url,
            'target': 'new',
        }
