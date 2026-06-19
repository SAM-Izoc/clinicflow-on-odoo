from odoo import models, fields, api

class ClinicFlowVisit(models.Model):
    _name = 'clinicflow.visit'
    _description = 'Veterinary Visit & SOAP Record'
    _order = 'date desc'

    name = fields.Char(string="Visit Reference", required=True, copy=False, readonly=True, default='New')
    pet_id = fields.Many2one('clinicflow.pet', string="Pet Patient", required=True)
    owner_id = fields.Many2one(related='pet_id.owner_id', string="Owner", readonly=True, store=True)
    vet_id = fields.Many2one('res.users', string="Veterinarian", default=lambda self: self.env.user)
    date = fields.Datetime(string="Visit Date", default=fields.Datetime.now, required=True)
    
    status = fields.Selection([
        ('booked', 'Booked'),
        ('check_in', 'Checked In'),
        ('waiting', 'Waiting'),
        ('consultation', 'Consultation'),
        ('treatment', 'Treatment'),
        ('billing', 'Billing Pending'),
        ('completed', 'Completed')
    ], string="Status", default='booked', required=True)

    # SOAP clinical documentation
    soap_s = fields.Text(string="Subjective (S)", help="Symptons, owner concerns, history")
    soap_o = fields.Text(string="Objective (O)", help="Physical exam findings, vitals, test results")
    soap_a = fields.Text(string="Assessment (A)", help="Diagnosis, differential diagnoses")
    soap_p = fields.Text(string="Plan (P)", help="Treatments, medications, follow-ups")

    event_id = fields.Many2one('calendar.event', string="Scheduled Appointment")
    charge_line_ids = fields.One2many('clinicflow.visit.charge.line', 'visit_id', string="Billing Charges")
    prescription_ids = fields.One2many('clinicflow.prescription', 'visit_id', string="Prescriptions")
    invoice_id = fields.Many2one('account.move', string="Related Invoice", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                today = fields.Datetime.now()
                vals['name'] = f"V-{today.strftime('%Y%m%d%H%M%S')}"
        visits = super().create(vals_list)
        for visit in visits:
            self.env['clinicflow.timeline.event'].create({
                'pet_id': visit.pet_id.id,
                'event_type': 'visit',
                'event_date': visit.date,
                'name': f"Visit Created: {visit.name} (Vet: {visit.vet_id.name or 'Unassigned'})",
                'res_model': 'clinicflow.visit',
                'res_id': visit.id
            })
        return visits

    def action_create_invoice(self):
        self.ensure_one()
        if self.invoice_id:
            return self.invoice_id

        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.owner_id.id,
            'pet_id': self.pet_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [],
        }

        # 1. Add Charges from charge_line_ids
        for charge in self.charge_line_ids:
            invoice_vals['invoice_line_ids'].append((0, 0, {
                'product_id': charge.product_id.id,
                'quantity': charge.quantity,
                'price_unit': charge.price_unit,
            }))

        # 2. Add Charges from Prescription Lines
        for prescription in self.prescription_ids:
            for line in prescription.line_ids:
                invoice_vals['invoice_line_ids'].append((0, 0, {
                    'product_id': line.product_id.id,
                    'quantity': line.quantity,
                    'price_unit': line.product_id.list_price,
                }))

        invoice = self.env['account.move'].create(invoice_vals)
        self.invoice_id = invoice.id

        # Generate timeline event for invoice
        self.env['clinicflow.timeline.event'].create({
            'pet_id': self.pet_id.id,
            'event_type': 'invoice',
            'event_date': fields.Datetime.now(),
            'name': f"Invoice Generated: {invoice.name or 'Draft Invoice'} (Amount: {invoice.amount_total})",
            'res_model': 'account.move',
            'res_id': invoice.id
        })
        return invoice


class ClinicFlowVisitChargeLine(models.Model):
    _name = 'clinicflow.visit.charge.line'
    _description = 'Visit Charge Line'

    visit_id = fields.Many2one('clinicflow.visit', string="Visit", required=True, ondelete='cascade')
    product_id = fields.Many2one(
        'product.product', 
        string="Service/Item", 
        domain="[('type', '=', 'service')]",
        required=True
    )
    quantity = fields.Float(string="Quantity", default=1.0, required=True)
    price_unit = fields.Float(string="Unit Price", related='product_id.list_price', readonly=False, store=True)

