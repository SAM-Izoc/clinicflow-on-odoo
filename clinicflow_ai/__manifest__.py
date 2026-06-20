{
    'name': 'ClinicFlow Vet AI Abstraction',
    'version': '1.0',
    'category': 'Services/Veterinary',
    'summary': 'Clinical Intelligence and Abstraction Layer for ClinicFlow',
    'author': 'Ali Raza',
    'website': 'https://clinicflow.ai',
    'depends': [
        'base',
        'clinicflow_core',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/visit_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'AGPL-3',
}
