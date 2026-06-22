{
    'name': 'ClinicFlow Vet Billing',
    'version': '1.0',
    'category': 'Services/Veterinary',
    'summary': 'Customer invoicing, pet integration, outstanding balance calculation, and financial dashboards for ClinicFlow.',
    'depends': [
        'clinicflow_clinical',
        'account',
    ],
    'data': [
        'views/pet_views.xml',
        'views/partner_views.xml',
        'views/report_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'AGPL-3',
}
