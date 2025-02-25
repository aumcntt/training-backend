from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HrPerformanceReview(models.Model):
    _name = 'hr.performance.review'
    _description = 'Performance Review'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    review_date = fields.Date(string='Review Date', required=True)
    reviewer_id = fields.Many2one('res.users', string='Reviewer', default=lambda self: self.env.user)
    performance_score = fields.Selection([
        ('1', 'Poor'),
        ('2', 'Average'),
        ('3', 'Good'),
        ('4', 'Excellent')
    ], string='Performance Score', required=True)
    comments = fields.Text(string='Comments')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved')
    ], string='Status', default='draft', tracking=True)

    @api.constrains('review_date')
    def _check_review_date(self):
        for record in self:
            if record.review_date < fields.Date.today():
                raise ValidationError("Review Date không thể ở quá khứ")

    def action_submit(self):
        for record in self:
            record.state = 'submitted'

    def action_approve(self):
        for record in self:
            record.state = 'approved'