{
    'name': 'Veterinary Hospital Management',
    'version': '19.0.1.0.0',
    'category': 'Healthcare',
    'sequence': 1,
    'author': 'Vaterny Hospital',
    'website': 'https://vaterny.com',
    'summary': 'Veterinary patients, appointments, medical records, and prescriptions',
    'description': 'Veterinary hospital management for Odoo 19 Community.',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'product',
        'sale',
        'account',
        'calendar',
        'contacts',
        'web',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',
        
        # Data
        'data/appointment_type_data.xml',
        'data/species_data.xml',
        'data/sequence_data.xml',
        
        # Views
        'views/owner_views.xml',
        'views/patient_views.xml',
        'views/appointment_views.xml',
        'views/medical_record_views.xml',
        'views/vital_sign_views.xml',
        'views/prescription_views.xml',
        'views/dashboard_views.xml',
        
        # Reports
        'reports/medical_record_report.xml',
        'reports/invoice_report.xml',
        'reports/appointment_report.xml',

        # Menus must load after all referenced actions.
        'views/menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'images': ['static/description/icon.png'],
}
