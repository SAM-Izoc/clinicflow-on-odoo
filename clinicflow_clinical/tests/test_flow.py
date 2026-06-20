from odoo.tests.common import TransactionCase
from odoo import fields
from odoo.exceptions import UserError
import datetime

class TestClinicFlowClinical(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create a partner/owner
        cls.owner = cls.env['res.partner'].create({
            'name': 'Test Owner',
            'is_pet_owner': True,
        })
        
        # Create a pet patient
        cls.pet = cls.env['clinicflow.pet'].create({
            'name': 'Buddy',
            'species': 'dog',
            'breed': 'Beagle',
            'gender': 'male',
            'owner_id': cls.owner.id,
        })
        
        # Create a product for consultation
        cls.consultation_product = cls.env['product.product'].create({
            'name': 'Standard Consultation',
            'type': 'service',
            'list_price': 50.0,
        })

    def test_01_appointment_checkin_flow(self):
        """ Tests that checking in a calendar appointment creates a visit SOAP note """
        # 1. Create a calendar appointment for Buddy
        now = fields.Datetime.now()
        appointment = self.env['calendar.event'].create({
            'name': 'Buddy Consultation',
            'start': now,
            'stop': now + datetime.timedelta(hours=1),
            'pet_id': self.pet.id,
            'appointment_status': 'scheduled',
        })
        
        # Verify initial state
        self.assertEqual(appointment.appointment_status, 'scheduled')
        self.assertFalse(appointment.visit_id)
        
        # 2. Check in the pet
        action = appointment.action_check_in_pet()
        
        # Verify visit was created and linked
        self.assertTrue(appointment.visit_id)
        self.assertEqual(appointment.appointment_status, 'checked_in')
        
        visit = appointment.visit_id
        self.assertEqual(visit.pet_id, self.pet)
        self.assertEqual(visit.status, 'check_in')
        
        # Verify redirect action
        self.assertEqual(action.get('res_model'), 'clinicflow.visit')
        self.assertEqual(action.get('res_id'), visit.id)

    def test_02_invoice_generation_flow(self):
        """ Tests that visit charge lines are correctly billed and generate Odoo invoices """
        # 1. Create a visit directly
        visit = self.env['clinicflow.visit'].create({
            'pet_id': self.pet.id,
            'status': 'consultation',
        })
        
        # 2. Add charge line
        charge = self.env['clinicflow.visit.charge.line'].create({
            'visit_id': visit.id,
            'product_id': self.consultation_product.id,
            'quantity': 1.0,
        })
        
        # Verify unit price links to product list price
        self.assertEqual(charge.price_unit, 50.0)
        
        # 3. Transition status to billing and create invoice
        visit.status = 'billing'
        invoice = visit.action_create_invoice()
        
        # Verify invoice is linked and has the correct fields
        self.assertEqual(visit.invoice_id, invoice)
        self.assertEqual(invoice.partner_id, self.owner)
        self.assertEqual(invoice.move_type, 'out_invoice')
        
        # Verify invoice line
        self.assertEqual(len(invoice.invoice_line_ids), 1)
        line = invoice.invoice_line_ids[0]
        self.assertEqual(line.product_id, self.consultation_product)
        self.assertEqual(line.quantity, 1.0)
        self.assertEqual(line.price_unit, 50.0)
