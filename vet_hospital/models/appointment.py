from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class Appointment(models.Model):
    _name = 'vet.appointment'
    _description = 'Veterinary Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_time desc'

    # Basic Information
    name = fields.Char(
        string='Appointment ID',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('vet.appointment')
    )
    
    appointment_type_id = fields.Many2one(
        'vet.appointment_type',
        string='Appointment Type',
        required=True,
        tracking=True
    )
    
    date_time = fields.Datetime(
        string='Date & Time',
        required=True,
        tracking=True
    )
    
    end_time = fields.Datetime(
        string='End Time',
        compute='_compute_end_time',
        store=True
    )
    
    duration = fields.Float(
        string='Duration (Minutes)',
        related='appointment_type_id.duration',
        readonly=True
    )
    
    # Patient & Owner
    patient_id = fields.Many2one(
        'vet.patient',
        string='Patient',
        required=True,
        tracking=True,
        ondelete='cascade'
    )
    
    owner_id = fields.Many2one(
        'res.partner',
        string='Owner',
        related='patient_id.owner_id',
        readonly=True,
        store=True
    )
    
    # Veterinarian
    vet_id = fields.Many2one(
        'res.partner',
        string='Veterinarian',
        required=True,
        domain="[('is_vet', '=', True)]",
        tracking=True
    )
    
    # Appointment Details
    reason = fields.Text(
        string='Reason for Visit',
        required=True,
        tracking=True
    )
    
    symptoms = fields.Text(string='Symptoms/Complaint')
    
    status = fields.Selection(
        [('scheduled', 'Scheduled'),
         ('confirmed', 'Confirmed'),
         ('in_progress', 'In Progress'),
         ('completed', 'Completed'),
         ('cancelled', 'Cancelled'),
         ('no_show', 'No Show')],
        string='Status',
        default='scheduled',
        tracking=True
    )
    
    # Communication
    reminder_sent = fields.Boolean(string='Reminder Sent')
    reminder_date = fields.Datetime(string='Reminder Date')
    
    notes = fields.Text(string='Notes')
    
    # Medical Record Link
    medical_record_id = fields.Many2one(
        'vet.medical_record',
        string='Medical Record',
        ondelete='set null'
    )
    
    # Invoice
    invoice_id = fields.Many2one(
        'account.move',
        string='Invoice',
        readonly=True
    )
    
    @api.depends('date_time', 'duration')
    def _compute_end_time(self):
        for appointment in self:
            if appointment.date_time and appointment.duration:
                appointment.end_time = appointment.date_time + timedelta(minutes=appointment.duration)
            else:
                appointment.end_time = appointment.date_time
    
    @api.constrains('date_time')
    def _check_appointment_conflict(self):
        """Check for appointment conflicts"""
        for appointment in self:
            if appointment.date_time:
                conflicting = self.search([
                    ('vet_id', '=', appointment.vet_id.id),
                    ('date_time', '=', appointment.date_time),
                    ('status', '!=', 'cancelled'),
                    ('id', '!=', appointment.id)
                ])
                if conflicting:
                    raise ValidationError(
                        f"Time slot already booked for {appointment.vet_id.name}"
                    )
    
    def action_confirm(self):
        """Confirm appointment"""
        for appointment in self:
            appointment.status = 'confirmed'
            appointment._send_confirmation()
    
    def action_start(self):
        """Start appointment"""
        for appointment in self:
            appointment.status = 'in_progress'
    
    def action_complete(self):
        """Complete appointment"""
        for appointment in self:
            appointment.status = 'completed'
    
    def action_cancel(self):
        """Cancel appointment"""
        for appointment in self:
            appointment.status = 'cancelled'
    
    def action_no_show(self):
        """Mark as no-show"""
        for appointment in self:
            appointment.status = 'no_show'
    
    def _send_confirmation(self):
        """Send confirmation email to owner"""
        template = self.env.ref('vet_hospital.email_template_appointment_confirmation', raise_if_not_found=False)
        if template:
            for appointment in self:
                template.send_mail(appointment.id, force_send=True)
    
    def send_reminder(self):
        """Send reminder email"""
        for appointment in self:
            if appointment.reminder_sent:
                continue
            
            template = self.env.ref('vet_hospital.email_template_appointment_reminder', raise_if_not_found=False)
            if template:
                template.send_mail(appointment.id, force_send=True)
                appointment.reminder_sent = True
                appointment.reminder_date = fields.Datetime.now()
    
    def action_create_medical_record(self):
        """Create medical record from appointment"""
        self.ensure_one()
        
        medical_record = self.env['vet.medical_record'].create({
            'appointment_id': self.id,
            'patient_id': self.patient_id.id,
            'vet_id': self.vet_id.id,
            'date_time': self.date_time,
        })
        
        self.medical_record_id = medical_record.id
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Medical Record',
            'res_model': 'vet.medical_record',
            'res_id': medical_record.id,
            'view_mode': 'form',
        }


class AppointmentType(models.Model):
    _name = 'vet.appointment_type'
    _description = 'Appointment Type'
    _order = 'name'

    name = fields.Char(string='Type Name', required=True)
    description = fields.Text(string='Description')
    duration = fields.Float(
        string='Duration (Minutes)',
        default=30,
        required=True
    )
    price = fields.Float(string='Default Price')
    category = fields.Selection(
        [('wellness', 'Wellness Check'),
         ('surgery', 'Surgery'),
         ('dental', 'Dental'),
         ('vaccination', 'Vaccination'),
         ('treatment', 'Treatment'),
         ('emergency', 'Emergency'),
         ('follow_up', 'Follow-up'),
         ('other', 'Other')],
        string='Category',
        default='wellness'
    )
    
    active = fields.Boolean(string='Active', default=True)

    _name_unique = models.Constraint(
        'unique(name)',
        'The appointment type name must be unique.',
    )
