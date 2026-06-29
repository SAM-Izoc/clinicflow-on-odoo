from odoo import models, fields, api


class Owner(models.Model):
    _inherit = 'res.partner'

    is_owner = fields.Boolean(
        string='Is Pet Owner',
        default=False,
        help='Mark this contact as a pet owner'
    )
    
    # Contact Details
    mobile = fields.Char(string='Mobile')
    emergency_contact = fields.Char(string='Emergency Contact')
    emergency_phone = fields.Char(string='Emergency Phone')
    
    # Preferences
    preferred_vet_id = fields.Many2one(
        'res.partner',
        string='Preferred Veterinarian',
        domain="[('is_vet', '=', True)]"
    )
    notification_method = fields.Selection(
        [('email', 'Email'), ('sms', 'SMS'), ('both', 'Both'), ('none', 'None')],
        string='Notification Method',
        default='email'
    )
    
    # Relationships
    patient_ids = fields.One2many(
        'vet.patient',
        'owner_id',
        string='Pets/Patients'
    )
    
    # Statistics
    total_patients = fields.Integer(
        string='Total Patients',
        compute='_compute_total_patients'
    )
    total_spent = fields.Float(
        string='Total Spent',
        compute='_compute_total_spent'
    )
    
    @api.depends('patient_ids')
    def _compute_total_patients(self):
        for owner in self:
            owner.total_patients = len(owner.patient_ids)
    
    @api.depends('patient_ids.medical_record_ids.invoice_id.amount_total')
    def _compute_total_spent(self):
        for owner in self:
            owner.total_spent = sum(
                record.invoice_id.amount_total
                for patient in owner.patient_ids
                for record in patient.medical_record_ids
                if record.invoice_id
            )
    
    def action_view_patients(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Patients',
            'res_model': 'vet.patient',
            'view_mode': 'list,form',
            'domain': [('owner_id', '=', self.id)],
            'context': {'default_owner_id': self.id},
        }


class Veterinarian(models.Model):
    _inherit = 'res.partner'

    is_vet = fields.Boolean(
        string='Is Veterinarian',
        default=False
    )
    
    specialization = fields.Selection(
        [('general', 'General Practice'),
         ('surgery', 'Surgery'),
         ('dentistry', 'Dentistry'),
         ('exotic', 'Exotic Animals'),
         ('dermatology', 'Dermatology'),
         ('cardiology', 'Cardiology'),
         ('orthopedics', 'Orthopedics')],
        string='Specialization'
    )
    
    license_number = fields.Char(string='License Number')
    license_expiry = fields.Date(string='License Expiry')
    
    appointment_ids = fields.One2many(
        'vet.appointment',
        'vet_id',
        string='Appointments'
    )
    
    medical_record_ids = fields.One2many(
        'vet.medical_record',
        'vet_id',
        string='Medical Records'
    )
    
    # Working Hours
    monday_from = fields.Float(string='Monday From')
    monday_to = fields.Float(string='Monday To')
    tuesday_from = fields.Float(string='Tuesday From')
    tuesday_to = fields.Float(string='Tuesday To')
    wednesday_from = fields.Float(string='Wednesday From')
    wednesday_to = fields.Float(string='Wednesday To')
    thursday_from = fields.Float(string='Thursday From')
    thursday_to = fields.Float(string='Thursday To')
    friday_from = fields.Float(string='Friday From')
    friday_to = fields.Float(string='Friday To')
    saturday_from = fields.Float(string='Saturday From')
    saturday_to = fields.Float(string='Saturday To')
    sunday_from = fields.Float(string='Sunday From')
    sunday_to = fields.Float(string='Sunday To')
    
    def get_availability(self, date):
        """Get vet availability for a specific date"""
        day_name = date.strftime('%A').lower()
        from_field = f'{day_name}_from'
        to_field = f'{day_name}_to'
        
        if hasattr(self, from_field) and hasattr(self, to_field):
            return {
                'from': getattr(self, from_field),
                'to': getattr(self, to_field)
            }
        return None
