from odoo import models, fields, api


class MedicalRecord(models.Model):
    _name = 'vet.medical_record'
    _description = 'Medical Record (SOAP)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_time desc'

    # Basic Information
    name = fields.Char(
        string='Record ID',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('vet.medical_record')
    )
    
    date_time = fields.Datetime(
        string='Date & Time',
        required=True,
        default=fields.Datetime.now,
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
        string='Veterinarian',
        required=True,
        domain="[('is_vet', '=', True)]",
        tracking=True
    )
    
    appointment_id = fields.Many2one(
        'vet.appointment',
        string='Appointment',
        ondelete='set null'
    )
    
    # SOAP Format
    subjective = fields.Text(
        string='Subjective (Chief Complaint)',
        help='Patient history and owner-reported symptoms'
    )
    
    objective = fields.Text(
        string='Objective (Physical Exam)',
        help='Observed signs and physical examination findings'
    )
    
    assessment = fields.Text(
        string='Assessment (Diagnosis)',
        help='Diagnosis or differential diagnosis'
    )
    
    plan = fields.Text(
        string='Plan (Treatment)',
        help='Treatment plan and recommendations'
    )
    
    # Diagnosis
    diagnosis_ids = fields.Many2many(
        'vet.diagnosis',
        string='Diagnoses'
    )
    
    primary_diagnosis_id = fields.Many2one(
        'vet.diagnosis',
        string='Primary Diagnosis'
    )
    
    # Clinical Findings
    body_condition_score = fields.Selection(
        [('1', '1 - Emaciated'),
         ('2', '2 - Underweight'),
         ('3', '3 - Ideal'),
         ('4', '4 - Overweight'),
         ('5', '5 - Obese')],
        string='Body Condition Score'
    )
    
    # Prescriptions
    prescription_ids = fields.One2many(
        'vet.prescription',
        'medical_record_id',
        string='Prescriptions'
    )

    vital_sign_ids = fields.One2many(
        'vet.vital_sign',
        'medical_record_id',
        string='Vital Signs'
    )

    # Lab Results & Attachments
    lab_result_ids = fields.One2many(
        'vet.lab_result',
        'medical_record_id',
        string='Lab Results'
    )
    
    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Attachments',
        help='X-rays, lab reports, etc.'
    )
    
    # Billing
    invoice_id = fields.Many2one(
        'account.move',
        string='Invoice',
        readonly=True
    )
    
    # Follow-up
    follow_up_required = fields.Boolean(string='Follow-up Required')
    follow_up_date = fields.Date(string='Follow-up Date')
    follow_up_notes = fields.Text(string='Follow-up Notes')
    
    # Status
    status = fields.Selection(
        [('draft', 'Draft'),
         ('completed', 'Completed'),
         ('archived', 'Archived')],
        string='Status',
        default='draft',
        tracking=True
    )
    
    notes = fields.Text(string='Additional Notes')
    
    def action_complete(self):
        """Mark as completed"""
        for record in self:
            record.status = 'completed'
    
    def action_archive(self):
        """Archive record"""
        for record in self:
            record.status = 'archived'
    
    def action_create_invoice(self):
        """Create invoice from medical record"""
        self.ensure_one()
        
        invoice_lines = []
        for prescription in self.prescription_ids.filtered(lambda p: p.product_id):
            invoice_lines.append((0, 0, {
                'product_id': prescription.product_id.id,
                'quantity': prescription.quantity,
                'price_unit': prescription.product_id.list_price,
            }))
        
        # Add service charge
        invoice_lines.append((0, 0, {
            'name': 'Veterinary Consultation',
            'quantity': 1,
            'price_unit': self.appointment_id.appointment_type_id.price or 50,
        }))
        
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.owner_id.id,
            'invoice_line_ids': invoice_lines,
            'ref': self.name,
        })
        
        self.invoice_id = invoice.id
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
        }


class Diagnosis(models.Model):
    _name = 'vet.diagnosis'
    _description = 'Medical Diagnosis'
    _order = 'name'

    name = fields.Char(string='Diagnosis Name', required=True)
    code = fields.Char(string='Diagnosis Code')
    description = fields.Text(string='Description')
    category = fields.Selection(
        [('infection', 'Infection'),
         ('injury', 'Injury'),
         ('disease', 'Disease'),
         ('genetic', 'Genetic'),
         ('behavioral', 'Behavioral'),
         ('other', 'Other')],
        string='Category'
    )
    
    active = fields.Boolean(string='Active', default=True)

    _name_unique = models.Constraint(
        'unique(name)',
        'The diagnosis name must be unique.',
    )


class LabResult(models.Model):
    _name = 'vet.lab_result'
    _description = 'Laboratory Result'

    name = fields.Char(string='Test Name', required=True)
    test_type = fields.Selection(
        [('blood', 'Blood Work'),
         ('urine', 'Urinalysis'),
         ('culture', 'Culture'),
         ('imaging', 'Imaging'),
         ('other', 'Other')],
        string='Test Type'
    )
    
    date = fields.Date(string='Test Date', required=True)
    result = fields.Text(string='Result')
    reference_value = fields.Char(string='Reference Value')
    status = fields.Selection(
        [('normal', 'Normal'),
         ('abnormal', 'Abnormal'),
         ('critical', 'Critical')],
        string='Status'
    )
    
    medical_record_id = fields.Many2one(
        'vet.medical_record',
        string='Medical Record',
        ondelete='cascade'
    )
    
    attachment_id = fields.Many2one(
        'ir.attachment',
        string='Lab Report'
    )
