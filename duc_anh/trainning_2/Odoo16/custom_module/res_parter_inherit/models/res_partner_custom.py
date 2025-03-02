from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_student = fields.Boolean(string='Là sinh viên' , default=False)
    student_ids = fields.Many2one("student.student", string='Mã sinh viên')

    _sql_constraints = [
        ('unique_student_id',
         'unique(student_ids)',
         'Mỗi sinh viên chỉ có một liên he.')
    ]

    @api.onchange('is_student')
    def _onchange_is_student(self):
        if not self.is_student:
            self.student_ids = None