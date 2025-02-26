from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


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
    ], string='Status', default='draft', tracking=True , readonly=True)

    @api.constrains('review_date')
    def _check_review_date(self):
        for record in self:
            if record.review_date < fields.Date.today():
                raise ValidationError("Review Date không thể ở quá khứ")

    def check_approved(self, record):
        if self.env.user == record.reviewer_id and self.env.user.has_group('hr.group_hr_manager'):
            return
        if not self.env.user.has_group('base.group_system'):
            raise UserError("Only managers can approve this review.")

    def unlink(self):
        for record in self:
            if  record.state in ['submitted', 'approved'] and not self.env.user.has_group('base.group_system'):
                raise UserError("You cannot delete this review.")

        return super(HrPerformanceReview, self).unlink()

    def write(self, vals):
        for record in self:
            if 'state' in vals and vals['state'] == 'approved':
                self.check_approved(record)
            else:
                if record.state in ['submitted', 'approved'] and not self.env.user.has_group('base.group_system'):
                    raise UserError("Only the admin can edit this review.")

        return super(HrPerformanceReview, self).write(vals)

    def action_submit(self):
        for record in self:
            record.state = 'submitted'

    def action_approve(self):
        for record in self:
            self.check_approved(record)
            record.state = 'approved'
