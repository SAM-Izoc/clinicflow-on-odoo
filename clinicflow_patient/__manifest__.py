{
    'name': 'ClinicFlow Vet Patient',
    'version': '1.0',
    'category': 'Services/Veterinary',
    'summary': 'Patient profiles and weight history for ClinicFlow Vet OS',
    'depends': [
        'clinicflow_core',
        'contacts',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/pet_views.xml',
        'views/partner_views.xml',
        'views/weight_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'AGPL-3',
}
