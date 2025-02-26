{
    'name': 'Performance Review for Employees',
    'version': '1.0',
    'category': 'Human Resources',
    'author': 'Your Name',
    'depends': ['hr', 'base', 'hr_performance'],
    'data': [
        'views/hr_performance_review_view.xml',
        'views/hr_employ_view_extension.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
