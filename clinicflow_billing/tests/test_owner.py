from odoo.tests.common import TransactionCase
from odoo import fields

class TestClinicFlowOwner(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create partner
        cls.owner = cls.env['res.partner'].create({
            'name': 'John Owner',
            'is_pet_owner': True,
        })
        
        # Create pets
        cls.pet1 = cls.env['clinicflow.pet'].create({
            'name': 'Max',
            'species': 'dog',
            'owner_id': cls.owner.id,
        })
        
        cls.pet2 = cls.env['clinicflow.pet'].create({
            'name': 'Bella',
            'species': 'cat',
            'owner_id': cls.owner.id,
        })

        # Create standard product
        cls.product = cls.env['product.product'].create({
            'name': 'Treatment Service',
            'type': 'service',
            'list_price': 100.0,
        })

    def test_01_owner_pet_count(self):
        """ Test that pet count calculates correctly for the owner """
        self.owner._compute_pet_stats()
        self.assertEqual(self.owner.pet_count, 2)

    def test_02_owner_total_outstanding_balance(self):
        """ Test that owner's total outstanding balance is aggregated correctly across all pets """
        # Verify initial states
        self.owner._compute_total_outstanding_balance()
        self.assertEqual(self.owner.total_outstanding_balance, 0.0)

        # Create a draft invoice for pet1
        invoice1 = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.owner.id,
            'pet_id': self.pet1.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 1.0,
                'price_unit': 80.0,
            })],
        })
        
        # Balance should still be 0 (invoices are draft)
        self.pet1._compute_billing_quick_info()
        self.owner._compute_total_outstanding_balance()
        self.assertEqual(self.owner.total_outstanding_balance, 0.0)

        # Simulate posting invoice 1
        invoice1.write({
            'state': 'posted',
            'payment_state': 'not_paid',
            'amount_residual': 80.0,
        })
        
        self.pet1.invalidate_model(['outstanding_balance'])
        self.pet1._compute_billing_quick_info()
        self.owner.invalidate_model(['total_outstanding_balance'])
        self.owner._compute_total_outstanding_balance()
        self.assertEqual(self.owner.total_outstanding_balance, invoice1.amount_residual)

        # Create and post invoice 2 for pet2
        invoice2 = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.owner.id,
            'pet_id': self.pet2.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 1.0,
                'price_unit': 120.0,
            })],
        })
        invoice2.write({
            'state': 'posted',
            'payment_state': 'not_paid',
            'amount_residual': 120.0,
        })
        
        self.pet2.invalidate_model(['outstanding_balance'])
        self.pet2._compute_billing_quick_info()
        
        self.owner.invalidate_model(['total_outstanding_balance'])
        self.owner._compute_total_outstanding_balance()
        
        expected_total = invoice1.amount_residual + invoice2.amount_residual
        self.assertEqual(self.owner.total_outstanding_balance, expected_total)
