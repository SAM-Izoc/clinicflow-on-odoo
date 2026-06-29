{
    'name': 'Veterinary Hospital - Merck Vet Manual Integration',
    'version': '19.0.1.0.0',
    'category': 'Healthcare',
    'summary': 'Merck Veterinary Manual links for veterinary workflows',
    'description': 'Adds contextual Merck Veterinary Manual links to the veterinary hospital module.',
    'author': 'Vaterny Hospital',
    'license': 'LGPL-3',
    'depends': ['vet_hospital', 'web'],
    'data': [
        'views/merck_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 2,
}
