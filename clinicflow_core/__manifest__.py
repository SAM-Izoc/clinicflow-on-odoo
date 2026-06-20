{
    'name': 'ClinicFlow Vet Core',
    'version': '1.0',
    'category': 'Services/Veterinary',
    'summary': 'Core Veterinary Practice Management for ClinicFlow Vet OS',
    'description': """
ClinicFlow Vet Core Module
==========================
This is the core veterinary operating system layer for ClinicFlow.
Provides base configurations and dashboards.
    """,
    'author': 'Ali Raza',
    'website': 'https://clinicflow.ai',
    'depends': [
        'base',
        'hr_attendance',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menus.xml',
        'views/dashboard_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
