{
    'name': 'ClinicFlow Vet Outreach & Reminders',
    'version': '1.0',
    'category': 'Services/Veterinary',
    'summary': 'Automated reminders, SMS/WhatsApp/Email templates, and owner outreach campaigns for ClinicFlow.',
    'depends': [
        'clinicflow_clinical',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/template_data.xml',
        'data/cron_data.xml',
        'views/res_config_settings_views.xml',
        'views/outreach_template_views.xml',
        'views/outreach_log_views.xml',
        'views/report_views_extension.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'AGPL-3',
}
