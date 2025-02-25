from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    performance_review_ids = fields.One2many(
        'hr.performance.review', 'employee_id', string='Performance Reviews')

    performance_review_count = fields.Integer(
        string='Performance Reviews Count',
        compute='_compute_performance_review_count'
    )

    average_performance_score = fields.Float(
        string='Average Performance Score',
        compute='_compute_average_performance_score',
        store=True,
    )

    @api.depends('performance_review_ids.state', 'performance_review_ids.performance_score')
    def _compute_average_performance_score(self):
        for employee in self:
            approved_reviews = self.env['hr.performance.review'].search([
                ('employee_id', '=', employee.id),
                ('state', '=', 'approved')
            ])

            if approved_reviews:
                total_score = 0
                for review in approved_reviews:
                    if review.performance_score == '1':
                        total_score += 1
                    elif review.performance_score == '2':
                        total_score += 2
                    elif review.performance_score == '3':
                        total_score += 3
                    elif review.performance_score == '4':
                        total_score += 4
                employee.average_performance_score = total_score / len(approved_reviews)
            else:
                employee.average_performance_score = 0.0

    @api.depends('performance_review_ids')
    def _compute_performance_review_count(self):
        for employee in self:
            employee.performance_review_count = len(employee.performance_review_ids)
