from odoo import models, fields, api


class VitalSign(models.Model):
    _name = 'vet.vital_sign'
    _description = 'Vital Signs'
    _order = 'date_time desc'

    patient_id = fields.Many2one(
        'vet.patient',
        string='Patient',
        required=True,
        ondelete='cascade'
    )
    
    medical_record_id = fields.Many2one(
        'vet.medical_record',
        string='Medical Record',
        ondelete='set null'
    )
    
    vet_id = fields.Many2one(
        'res.partner',
        string='Recorded By',
        domain="[('is_vet', '=', True)]"
    )
    
    date_time = fields.Datetime(
        string='Date & Time',
        required=True,
        default=fields.Datetime.now
    )
    
    # Temperature
    temperature = fields.Float(
        string='Temperature (°C)',
        help='Normal: 37.5-39°C'
    )
    temperature_normal = fields.Boolean(
        string='Temperature Normal',
        compute='_compute_temperature_normal',
        store=True
    )
    
    # Heart Rate
    heart_rate = fields.Float(
        string='Heart Rate (bpm)',
        help='Normal: 60-100 bpm for dogs, 110-130 bpm for cats'
    )
    heart_rate_normal = fields.Boolean(
        string='Heart Rate Normal',
        compute='_compute_heart_rate_normal',
        store=True
    )
    
    # Respiration
    respiration = fields.Float(
        string='Respiration (breaths/min)',
        help='Normal: 10-30 bpm'
    )
    respiration_normal = fields.Boolean(
        string='Respiration Normal',
        compute='_compute_respiration_normal',
        store=True
    )
    
    # Blood Pressure
    systolic = fields.Float(string='Systolic (mmHg)')
    diastolic = fields.Float(string='Diastolic (mmHg)')
    blood_pressure_normal = fields.Boolean(
        string='Blood Pressure Normal',
        compute='_compute_blood_pressure_normal',
        store=True
    )
    
    # Weight
    weight = fields.Float(
        string='Weight (kg)',
        help='Current weight of patient'
    )
    weight_change = fields.Float(
        string='Weight Change (kg)',
        compute='_compute_weight_change'
    )
    
    # Mucous Membranes
    mucous_membrane_color = fields.Selection(
        [('pink', 'Pink'),
         ('pale', 'Pale'),
         ('red', 'Red'),
         ('yellow', 'Yellow'),
         ('blue', 'Blue')],
        string='Mucous Membrane Color'
    )
    
    capillary_refill_time = fields.Float(
        string='Capillary Refill Time (sec)',
        help='Normal: <2 seconds'
    )
    
    # Hydration
    skin_turgor = fields.Selection(
        [('normal', 'Normal'),
         ('mild_dehydration', 'Mild Dehydration'),
         ('moderate_dehydration', 'Moderate Dehydration'),
         ('severe_dehydration', 'Severe Dehydration')],
        string='Skin Turgor'
    )
    
    # Attitude/Behavior
    attitude = fields.Selection(
        [('alert', 'Alert'),
         ('anxious', 'Anxious'),
         ('depressed', 'Depressed'),
         ('lethargic', 'Lethargic'),
         ('comatose', 'Comatose')],
        string='Attitude'
    )
    
    body_condition_score = fields.Selection(
        [('1', '1 - Emaciated'),
         ('2', '2 - Underweight'),
         ('3', '3 - Ideal'),
         ('4', '4 - Overweight'),
         ('5', '5 - Obese')],
        string='Body Condition Score'
    )
    
    # Additional Notes
    abnormalities = fields.Text(string='Abnormalities/Concerns')
    notes = fields.Text(string='Notes')
    
    @api.depends('temperature')
    def _compute_temperature_normal(self):
        for vital in self:
            if vital.temperature:
                # Normal temp for most pets: 37.5-39°C
                vital.temperature_normal = 37.5 <= vital.temperature <= 39.0
            else:
                vital.temperature_normal = False
    
    @api.depends('heart_rate', 'patient_id')
    def _compute_heart_rate_normal(self):
        for vital in self:
            if vital.heart_rate:
                if vital.patient_id.species_id.name in ['Feline', 'Cat']:
                    # Cats: 110-130 bpm
                    vital.heart_rate_normal = 110 <= vital.heart_rate <= 140
                else:
                    # Dogs: 60-100 bpm
                    vital.heart_rate_normal = 60 <= vital.heart_rate <= 100
            else:
                vital.heart_rate_normal = False
    
    @api.depends('respiration')
    def _compute_respiration_normal(self):
        for vital in self:
            if vital.respiration:
                # Normal: 10-30 breaths/min
                vital.respiration_normal = 10 <= vital.respiration <= 30
            else:
                vital.respiration_normal = False
    
    @api.depends('systolic', 'diastolic')
    def _compute_blood_pressure_normal(self):
        for vital in self:
            if vital.systolic and vital.diastolic:
                # Normal: <120/80 mmHg
                vital.blood_pressure_normal = vital.systolic < 120 and vital.diastolic < 80
            else:
                vital.blood_pressure_normal = False
    
    @api.depends('weight', 'patient_id')
    def _compute_weight_change(self):
        for vital in self:
            if vital.weight:
                previous_vital = self.search([
                    ('patient_id', '=', vital.patient_id.id),
                    ('date_time', '<', vital.date_time),
                    ('weight', '!=', False)
                ], limit=1, order='date_time desc')
                
                if previous_vital:
                    vital.weight_change = vital.weight - previous_vital.weight
                else:
                    vital.weight_change = 0
            else:
                vital.weight_change = 0
    
    def get_abnormality_alert(self):
        """Return list of abnormal vitals"""
        alerts = []
        if not self.temperature_normal:
            alerts.append(f"Temperature: {self.temperature}°C")
        if not self.heart_rate_normal:
            alerts.append(f"Heart Rate: {self.heart_rate} bpm")
        if not self.respiration_normal:
            alerts.append(f"Respiration: {self.respiration} breaths/min")
        if not self.blood_pressure_normal and self.systolic:
            alerts.append(f"BP: {self.systolic}/{self.diastolic} mmHg")
        
        return alerts
