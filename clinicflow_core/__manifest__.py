{
    'name': 'ClinicFlow Vet Core',
    'version': '1.0',
    'category': 'Services/Veterinary',
    'summary': 'Core Veterinary Practice Management for ClinicFlow Vet OS',
    'description': """
ClinicFlow Vet Core Module
==========================
This is the core veterinary operating system layer for ClinicFlow.
Integrates custom veterinary concepts with native Odoo ERP modules:
- Pets & Owners (Contacts Integration)
- Veterinary Visits & SOAP notes (CRM/Calendar/Invoicing Integration)
- Prescriptions & Vaccinations (Inventory/Purchase Integration)
    """,
    'author': 'Ali Raza (https://github.com/amrshah/), Company: VexterSoft/Silver Ant Marketing',
    'website': 'https://clinicflow.ai',
    'depends': [
        'base',
        'contacts',
        'crm',
        'calendar',
        'stock',
        'purchase',
        'account',
        'hr_attendance',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menus.xml',
        'views/pet_views.xml',
        'views/visit_views.xml',
        'views/partner_views.xml',
        'views/admission_views.xml',
        'views/calendar_views.xml',
        'views/weight_views.xml',
        'views/dashboard_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
