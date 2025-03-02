{
    'name': 'student_manager',
    'version': '1.0',
    'category': 'Student',
    'summary': 'A custom module for learning purposes',
    'description': 'This module is a demonstration of creating a custom Odoo module.',
    'author': 'Your Name',
    'website': 'https://www.yourwebsite.com',
    'depends': ['contacts'],
    'data': [
        'views/student_view.xml',
        'views/library_book_view.xml',
        'security/ir.model.access.csv'
    ],
    'application': True,
    'installable': True,
}
