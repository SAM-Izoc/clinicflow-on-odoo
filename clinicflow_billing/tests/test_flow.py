from odoo.tests.common import TransactionCase
from odoo import fields
import datetime

class TestClinicFlowBilling(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create a partner/owner
        cls.owner = cls.env['res.partner'].create({
            'name': 'Billing Test Owner',
            'is_pet_owner': True,
        })
        
        # Create a pet patient
        cls.pet = cls.env['clinicflow.pet'].create({
            'name': 'Max',
            'species': 'cat',
            'breed': 'Siamese',
            'gender': 'female',
            'owner_id': cls.owner.id,
        })
        
        # Create a product for consultation
        cls.consultation_product = cls.env['product.product'].create({
            'name': 'Standard Consultation',
            'type': 'service',
            'list_price': 60.0,
        })

    def test_01_invoice_pet_linkage(self):
        """ Test that creating an invoice from a visit sets the pet_id on account.move """
        visit = self.env['clinicflow.visit'].create({
            'pet_id': self.pet.id,
            'status': 'consultation',
        })
        
        self.env['clinicflow.visit.charge.line'].create({
            'visit_id': visit.id,
            'product_id': self.consultation_product.id,
            'quantity': 1.0,
        })
        
        visit.status = 'billing'
        invoice = visit.action_create_invoice()
        
        # Check linkage
        self.assertEqual(visit.invoice_id, invoice)
        self.assertEqual(invoice.pet_id, self.pet)
        self.assertEqual(invoice.partner_id, self.owner)

    def test_02_outstanding_balance_calculation(self):
        """ Test outstanding balance computation on pet based on linked invoices """
        # Initial balance should be 0
        self.pet._compute_billing_quick_info()
        self.assertEqual(self.pet.outstanding_balance, 0.0)
        
        # Create a draft invoice (state='draft')
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.owner.id,
            'pet_id': self.pet.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.consultation_product.id,
                'quantity': 1.0,
                'price_unit': 100.0,
            })],
        }
        invoice = self.env['account.move'].create(invoice_vals)
        
        # Since state is 'draft', outstanding balance should still be 0.0
        self.pet._compute_billing_quick_info()
        self.assertEqual(self.pet.outstanding_balance, 0.0)
        
        # Post the invoice (or simulate posted state and residual amount for testing)
        # Note: actually posting may require a complex chart of accounts setup, so we can write to fields
        # if the test environment allows, or just test our compute method works.
        # In Odoo, state and amount_residual can be set directly in a test environment to test downstream logic.
        invoice.write({
            'state': 'posted',
            'payment_state': 'not_paid',
            'amount_residual': 100.0,
        })
        
        # Recompute outstanding balance
        self.pet.invalidate_model(['outstanding_balance'])
        self.pet._compute_billing_quick_info()
        self.assertEqual(self.pet.outstanding_balance, invoice.amount_residual)
