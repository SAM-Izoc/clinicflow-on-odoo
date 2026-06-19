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

    # Persistent Health Info
    emergency_contact = fields.Char(string="Emergency Contact")
    alerts = fields.Text(string="Clinical Alerts")
    chronic_conditions = fields.Text(string="Chronic Conditions")
    allergies = fields.Text(string="Allergies")
    surgical_history = fields.Text(string="Surgical History")

    # Computed fields
    age_display = fields.Char(string="Age", compute="_compute_age_display")
    
    # Weight metrics
    weight_count = fields.Integer(string="Weight Count", compute="_compute_weight_metrics")
    last_weight = fields.Float(string="Last Weight", compute="_compute_weight_metrics")
    last_weight_display = fields.Char(string="Last Weight Display", compute="_compute_weight_metrics")

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

    @api.depends('weight_ids')
    def _compute_weight_metrics(self):
        for rec in self:
            weights = rec.weight_ids.sorted(key=lambda w: (w.date, w.id), reverse=True)
            rec.weight_count = len(weights)
            if weights:
                latest = weights[0]
                rec.last_weight = latest.weight
                days_ago = (fields.Date.today() - latest.date).days
                if days_ago == 0:
                    days_text = "today"
                elif days_ago == 1:
                    days_text = "yesterday"
                else:
                    days_text = f"{days_ago} days ago"
                rec.last_weight_display = f"{latest.weight} kg ({days_text})"
            else:
                rec.last_weight = 0.0
                rec.last_weight_display = "No records"

    @api.model
    def read(self, fields_to_read, load='_load'):
        """ Registers that this pet record was viewed to log recent patient activity """
        res = super().read(fields_to_read, load=load)
        if len(self) == 1 and self.env.user and not self.env.context.get('bin_size'):
            # Avoid logging on internal fields check
            if 'name' in fields_to_read or 'owner_id' in fields_to_read:
                self.env.user._add_recent_pet(self)
        return res

    # Smart button action helpers
    def action_view_weight_history(self):
        self.ensure_one()
        return {
            'name': f"Weight History - {self.name}",
            'type': 'ir.actions.act_window',
            'res_model': 'clinicflow.weight.record',
            'view_mode': 'graph,list',
            'domain': [('pet_id', '=', self.id)],
            'context': {'default_pet_id': self.id},
        }

    def action_view_invoices(self):
        self.ensure_one()
        return {
            'name': f"Invoices - {self.name}",
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('pet_id', '=', self.id)],
            'context': {'default_pet_id': self.id, 'default_move_type': 'out_invoice'},
        }

    # Quick action header helpers
    def action_create_appointment_quick(self):
        self.ensure_one()
        return {
            'name': 'New Appointment',
            'type': 'ir.actions.act_window',
            'res_model': 'calendar.event',
            'view_mode': 'form',
            'context': {
                'default_pet_id': self.id,
                'default_name': f"Consultation: {self.name}",
                'default_partner_ids': [self.owner_id.id] if self.owner_id else [],
            },
            'target': 'new',
        }

    def action_create_visit_quick(self):
        self.ensure_one()
        return {
            'name': 'New Visit SOAP',
            'type': 'ir.actions.act_window',
            'res_model': 'clinicflow.visit',
            'view_mode': 'form',
            'context': {
                'default_pet_id': self.id,
                'default_status': 'consultation',
            },
        }

    def action_create_prescription_quick(self):
        self.ensure_one()
        active_visit = self.env['clinicflow.visit'].search([
            ('pet_id', '=', self.id), 
            ('status', 'not in', ['completed', 'booked'])
        ], limit=1)
        return {
            'name': 'New Prescription',
            'type': 'ir.actions.act_window',
            'res_model': 'clinicflow.prescription',
            'view_mode': 'form',
            'context': {
                'default_pet_id': self.id,
                'default_visit_id': active_visit.id if active_visit else False,
            },
            'target': 'new',
        }

    def action_create_vaccination_quick(self):
        self.ensure_one()
        return {
            'name': 'New Vaccination',
            'type': 'ir.actions.act_window',
            'res_model': 'clinicflow.vaccination',
            'view_mode': 'form',
            'context': {
                'default_pet_id': self.id,
            },
            'target': 'new',
        }

    def action_create_admission_quick(self):
        self.ensure_one()
        active_visit = self.env['clinicflow.visit'].search([
            ('pet_id', '=', self.id), 
            ('status', 'not in', ['completed', 'booked'])
        ], limit=1)
        return {
            'name': 'New Hospitalization',
            'type': 'ir.actions.act_window',
            'res_model': 'clinicflow.admission',
            'view_mode': 'form',
            'context': {
                'default_pet_id': self.id,
                'default_visit_id': active_visit.id if active_visit else False,
            },
            'target': 'new',
        }
