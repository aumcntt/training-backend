{
    'name': 'Performance Review for Employees',
    'version': '1.0',
    'category': 'Human Resources',
    'author': 'Your Name',
    'depends': ['hr', 'base'],
    'data': [
        'views/hr_employ_view_extension.xml',
        'wizard/employee_skill_wizard.xml',
        'views/employee_certification.xml',
        'views/employee_skill.xml',
        'security/security.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}