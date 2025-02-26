{
    'name': 'HR Performance Review',
    'version': '1.0',
    'depends': ['hr', 'base'],
    'data': [
        'views/performance_review_views.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'demo/hr_performance_demo.xml',
    ],
    'installable': True,
    'application': True,
}
