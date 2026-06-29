from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Prescription(models.Model):
    _name = 'vet.prescription'
    _description = 'Prescription'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    # Basic Information
    name = fields.Char(
        string='Prescription ID',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('vet.prescription')
    )
    
    date = fields.Date(
        string='Prescription Date',
        required=True,
        default=fields.Date.today,
        tracking=True
    )
    
    # Patient & Provider
    patient_id = fields.Many2one(
        'vet.patient',
        string='Patient',
        required=True,
        ondelete='cascade',
        tracking=True
    )
    
    owner_id = fields.Many2one(
        'res.partner',
        string='Owner',
        related='patient_id.owner_id',
        readonly=True,
        store=True
    )
    
    vet_id = fields.Many2one(
        'res.partner',
        string='Prescribed By',
        required=True,
        domain="[('is_vet', '=', True)]",
        tracking=True
    )
    
    medical_record_id = fields.Many2one(
        'vet.medical_record',
        string='Medical Record',
        ondelete='set null'
    )
    
    # Medication Details
    product_id = fields.Many2one(
        'product.product',
        string='Medication/Product',
        required=True,
        domain="[('is_medicine', '=', True)]"
    )
    
    medication_name = fields.Char(
        string='Medication Name',
        related='product_id.name',
        readonly=True
    )
    
    quantity = fields.Float(
        string='Quantity',
        required=True,
        default=1
    )
    
    unit_of_measure = fields.Char(
        string='Unit',
        related='product_id.uom_id.name',
        readonly=True
    )
    
    # Dosage & Instructions
    dosage = fields.Char(
        string='Dosage',
        required=True,
        help='e.g., 250mg'
    )
    
    frequency = fields.Selection(
        [('once_daily', 'Once Daily'),
         ('twice_daily', 'Twice Daily'),
         ('three_times_daily', 'Three Times Daily'),
         ('four_times_daily', 'Four Times Daily'),
         ('every_6_hours', 'Every 6 Hours'),
         ('every_8_hours', 'Every 8 Hours'),
         ('every_12_hours', 'Every 12 Hours'),
         ('as_needed', 'As Needed'),
         ('weekly', 'Weekly'),
         ('monthly', 'Monthly'),
         ('other', 'Other')],
        string='Frequency',
        required=True
    )
    
    custom_frequency = fields.Char(
        string='Custom Frequency',
        help='If frequency is "other"'
    )
    
    duration = fields.Float(
        string='Duration (Days)',
        help='Number of days to take medication'
    )
    
    instructions = fields.Text(
        string='Special Instructions',
        help='e.g., Take with food, Avoid dairy products'
    )
    
    # Route of Administration
    route = fields.Selection(
        [('oral', 'Oral (By Mouth)'),
         ('topical', 'Topical (On Skin)'),
         ('injection', 'Injection'),
         ('inhalation', 'Inhalation'),
         ('ophthalmic', 'Eye Drops'),
         ('otic', 'Ear Drops'),
         ('rectal', 'Rectal'),
         ('transdermal', 'Transdermal'),
         ('other', 'Other')],
        string='Route of Administration',
        required=True,
        default='oral'
    )
    
    # Refills
    refills = fields.Integer(
        string='Number of Refills',
        default=0
    )
    
    refills_remaining = fields.Integer(
        string='Refills Remaining',
        default=0
    )
    
    # Status
    status = fields.Selection(
        [('draft', 'Draft'),
         ('active', 'Active'),
         ('completed', 'Completed'),
         ('discontinued', 'Discontinued')],
        string='Status',
        default='draft',
        tracking=True
    )
    
    expiry_date = fields.Date(string='Expiry Date')
    
    # Side Effects & Warnings
    side_effects = fields.Text(string='Possible Side Effects')
    contraindications = fields.Text(string='Contraindications')
    drug_interactions = fields.Text(string='Drug Interactions')
    
    # Additional
    notes = fields.Text(string='Notes')
    is_controlled = fields.Boolean(
        string='Controlled Substance',
        related='product_id.is_controlled',
        readonly=True
    )
    
    def action_activate(self):
        """Activate prescription"""
        for prescription in self:
            prescription.status = 'active'
    
    def action_discontinue(self):
        """Discontinue prescription"""
        for prescription in self:
            prescription.status = 'discontinued'
    
    def action_refill(self):
        """Process refill"""
        for prescription in self:
            if prescription.refills_remaining > 0:
                prescription.refills_remaining -= 1
                # Create new prescription record or update quantity
            else:
                raise ValidationError("No refills remaining. Contact veterinarian.")
    
    def get_medication_label(self):
        """Generate medication label"""
        return f"""
        MEDICATION LABEL
        ================
        Patient: {self.patient_id.name}
        Owner: {self.owner_id.name}
        
        Medication: {self.medication_name}
        Dosage: {self.dosage}
        Frequency: {self.frequency}
        Route: {self.route}
        Duration: {self.duration} days
        
        Instructions: {self.instructions}
        
        Prescribed by: {self.vet_id.name}
        Date: {self.date}
        Expiry: {self.expiry_date}
        
        Side Effects: {self.side_effects}
        """


class MedicineProduct(models.Model):
    _inherit = 'product.template'
    
    is_medicine = fields.Boolean(
        string='Is Medicine/Drug',
        default=False
    )
    
    active_ingredient = fields.Char(string='Active Ingredient')
    strength = fields.Char(string='Strength')
    manufacturer = fields.Char(string='Manufacturer')
    
    is_controlled = fields.Boolean(
        string='Controlled Substance',
        default=False
    )
    
    requires_prescription = fields.Boolean(
        string='Requires Prescription',
        default=False
    )
    
    drug_classification = fields.Selection(
        [('otc', 'Over-the-Counter'),
         ('rx', 'Prescription Required'),
         ('controlled', 'Controlled Substance')],
        string='Classification'
    )
    
    approved_for_animals = fields.Selection(
        [('all', 'All Animals'),
         ('canine', 'Dogs Only'),
         ('feline', 'Cats Only'),
         ('other', 'Other')],
        string='Approved For'
    )
    
    min_dosage = fields.Char(string='Min Dosage')
    max_dosage = fields.Char(string='Max Dosage')
    
    contraindications = fields.Text(string='Contraindications')
    interactions = fields.Text(string='Drug Interactions')
