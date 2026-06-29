from odoo import models, fields, api
from datetime import datetime, timedelta


class Patient(models.Model):
    _name = 'vet.patient'
    _description = 'Patient (Animal)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'
    _rec_name = 'display_name'

    # Basic Information
    name = fields.Char(
        string='Pet Name',
        required=True,
        tracking=True
    )
    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True
    )
    
    microchip_id = fields.Char(
        string='Microchip ID',
        help='Unique microchip identification number'
    )
    
    # Species and Breed
    species_id = fields.Many2one(
        'vet.species',
        string='Species',
        required=True,
        tracking=True
    )
    
    breed_id = fields.Many2one(
        'vet.breed',
        string='Breed',
        domain="[('species_id', '=', species_id)]"
    )
    
    # Physical Characteristics
    color = fields.Char(string='Color/Markings')
    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Char(
        string='Age',
        compute='_compute_age',
        store=False
    )
    gender = fields.Selection(
        [('male', 'Male'),
         ('female', 'Female'),
         ('unknown', 'Unknown')],
        string='Gender'
    )
    
    is_neutered = fields.Boolean(string='Neutered/Spayed')
    neutered_date = fields.Date(string='Date Neutered')
    
    # Owner Information
    owner_id = fields.Many2one(
        'res.partner',
        string='Owner',
        required=True,
        tracking=True,
        domain="[('is_owner', '=', True)]"
    )
    
    # Medical Information
    weight = fields.Float(
        string='Weight (kg)',
        tracking=True
    )
    
    allergies = fields.Text(string='Allergies')
    medical_conditions = fields.Text(string='Medical Conditions')
    medications = fields.Text(string='Current Medications')
    diet = fields.Text(string='Diet/Food')
    
    # Veterinary Preferences
    preferred_vet_id = fields.Many2one(
        'res.partner',
        string='Preferred Veterinarian',
        domain="[('is_vet', '=', True)]"
    )
    
    primary_provider_id = fields.Many2one(
        'res.partner',
        string='Primary Provider',
        domain="[('is_vet', '=', True)]"
    )
    
    # Status
    status = fields.Selection(
        [('active', 'Active'),
         ('inactive', 'Inactive'),
         ('deceased', 'Deceased')],
        string='Status',
        default='active',
        tracking=True
    )
    
    date_deceased = fields.Date(string='Date of Death')
    
    # Relationships
    appointment_ids = fields.One2many(
        'vet.appointment',
        'patient_id',
        string='Appointments'
    )
    
    medical_record_ids = fields.One2many(
        'vet.medical_record',
        'patient_id',
        string='Medical Records'
    )
    
    vital_sign_ids = fields.One2many(
        'vet.vital_sign',
        'patient_id',
        string='Vital Signs'
    )
    
    prescription_ids = fields.One2many(
        'vet.prescription',
        'patient_id',
        string='Prescriptions'
    )
    
    # Statistics
    last_visit = fields.Date(
        string='Last Visit',
        compute='_compute_last_visit',
        store=True
    )
    
    next_appointment = fields.Date(
        string='Next Appointment',
        compute='_compute_next_appointment'
    )
    
    total_appointments = fields.Integer(
        string='Total Appointments',
        compute='_compute_total_appointments'
    )
    
    last_weight = fields.Float(
        string='Last Weight',
        compute='_compute_last_weight'
    )
    
    total_invoiced = fields.Float(
        string='Total Invoiced',
        compute='_compute_total_invoiced'
    )
    
    # Additional
    photo = fields.Image(string='Photo')
    notes = fields.Text(string='Notes')

    _microchip_id_unique = models.Constraint(
        'unique(microchip_id)',
        'The microchip ID must be unique.',
    )
    
    @api.depends('name', 'owner_id')
    def _compute_display_name(self):
        for patient in self:
            if patient.owner_id:
                patient.display_name = f"{patient.name} ({patient.owner_id.name})"
            else:
                patient.display_name = patient.name
    
    @api.depends('date_of_birth')
    def _compute_age(self):
        for patient in self:
            if patient.date_of_birth:
                today = fields.Date.today()
                birth = patient.date_of_birth
                age_days = (today - birth).days
                
                if age_days < 30:
                    patient.age = f"{age_days} days"
                elif age_days < 365:
                    months = age_days // 30
                    patient.age = f"{months} months"
                else:
                    years = age_days // 365
                    months = (age_days % 365) // 30
                    patient.age = f"{years} years {months} months" if months else f"{years} years"
            else:
                patient.age = "Unknown"
    
    @api.depends('appointment_ids.date_time')
    def _compute_last_visit(self):
        for patient in self:
            completed_appointments = patient.appointment_ids.filtered(
                lambda a: a.status == 'completed' and a.date_time
            ).sorted(key=lambda a: a.date_time, reverse=True)
            
            patient.last_visit = completed_appointments[0].date_time.date() if completed_appointments else None
    
    def _compute_next_appointment(self):
        for patient in self:
            future_appointments = patient.appointment_ids.filtered(
                lambda a: a.date_time >= datetime.now() and a.status != 'cancelled'
            ).sorted(key=lambda a: a.date_time)
            
            patient.next_appointment = future_appointments[0].date_time.date() if future_appointments else None
    
    def _compute_total_appointments(self):
        for patient in self:
            patient.total_appointments = len(patient.appointment_ids)
    
    @api.depends('vital_sign_ids.weight')
    def _compute_last_weight(self):
        for patient in self:
            last_vitals = patient.vital_sign_ids.sorted(
                key=lambda v: v.date_time, reverse=True
            )
            patient.last_weight = last_vitals[0].weight if last_vitals and last_vitals[0].weight else patient.weight
    
    def _compute_total_invoiced(self):
        for patient in self:
            patient.total_invoiced = sum(
                record.invoice_id.amount_total 
                for record in patient.medical_record_ids 
                if record.invoice_id
            )
    
    def action_view_appointments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'vet.appointment',
            'view_mode': 'list,form,calendar',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }
    
    def action_view_medical_records(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Medical Records',
            'res_model': 'vet.medical_record',
            'view_mode': 'list,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }


class Species(models.Model):
    _name = 'vet.species'
    _description = 'Animal Species'
    _order = 'name'

    name = fields.Char(string='Species Name', required=True)
    scientific_name = fields.Char(string='Scientific Name')
    description = fields.Text(string='Description')

    _name_unique = models.Constraint(
        'unique(name)',
        'The species name must be unique.',
    )
    
    breed_ids = fields.One2many(
        'vet.breed',
        'species_id',
        string='Breeds'
    )


class Breed(models.Model):
    _name = 'vet.breed'
    _description = 'Animal Breed'
    _order = 'name'

    name = fields.Char(string='Breed Name', required=True)
    species_id = fields.Many2one(
        'vet.species',
        string='Species',
        required=True,
        ondelete='cascade'
    )
    description = fields.Text(string='Description')
    average_weight = fields.Float(string='Average Weight (kg)')
    life_expectancy = fields.Integer(string='Life Expectancy (years)')
