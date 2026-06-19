from odoo import models, fields, api

class ClinicFlowPet(models.Model):
    _name = 'clinicflow.pet'
    _description = 'Veterinary Pet Patient'

    name = fields.Char(string="Pet Name", required=True)
    species = fields.Selection([
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('other', 'Other')
    ], string="Species", required=True, default='dog')
    breed = fields.Char(string="Breed")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('neutered_male', 'Neutered Male'),
        ('spayed_female', 'Spayed Female')
    ], string="Gender", default='male')
    dob = fields.Date(string="Date of Birth")
    microchip = fields.Char(string="Microchip Number")
    owner_id = fields.Many2one(
        'res.partner', 
        string="Owner", 
        domain="[('is_company', '=', False)]", 
        required=True
    )
    photo = fields.Image(string="Photo", max_width=256, max_height=256)
    notes = fields.Text(string="Medical Notes")

    # Persistent Health Info (CTO feedback)
    emergency_contact = fields.Char(string="Emergency Contact")
    alerts = fields.Text(string="Clinical Alerts")
    chronic_conditions = fields.Text(string="Chronic Conditions")
    allergies = fields.Text(string="Allergies")
    surgical_history = fields.Text(string="Surgical History")

    # Computed fields
    age_display = fields.Char(string="Age", compute="_compute_age_display")

    # One2many relations
    visit_ids = fields.One2many('clinicflow.visit', 'pet_id', string="Visits")
    vaccination_ids = fields.One2many('clinicflow.vaccination', 'pet_id', string="Vaccinations")
    prescription_ids = fields.One2many('clinicflow.prescription', 'pet_id', string="Prescriptions")
    admission_ids = fields.One2many('clinicflow.admission', 'pet_id', string="Hospitalizations")
    invoice_ids = fields.One2many('account.move', 'pet_id', string="Invoices")
    weight_ids = fields.One2many('clinicflow.weight.record', 'pet_id', string="Weight History")
    timeline_ids = fields.One2many('clinicflow.timeline.event', 'pet_id', string="Timeline Events")
    attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'clinicflow.pet')], string="Documents")

    @api.depends('dob')
    def _compute_age_display(self):
        for rec in self:
            if rec.dob:
                today = fields.Date.today()
                dob = rec.dob
                delta_y = today.year - dob.year
                delta_m = today.month - dob.month
                if today.day < dob.day:
                    delta_m -= 1
                if delta_m < 0:
                    delta_y -= 1
                    delta_m += 12
                
                if delta_y > 0:
                    rec.age_display = f"{delta_y} Year(s)" if delta_m == 0 else f"{delta_y} Year(s), {delta_m} Month(s)"
                else:
                    rec.age_display = f"{delta_m} Month(s)" if delta_m > 0 else "Newborn"
            else:
                rec.age_display = "Unknown"
