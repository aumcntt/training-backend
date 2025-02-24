from datetime import date

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class Student(models.Model):
    _name = 'student.student'
    _description = 'Student Information'

    name = fields.Char(string='Tên Sinh Viên', required=True)
    student_code = fields.Char(string='Mã Sinh Viên', required=True)
    display_name = fields.Char(string='Tên Hiển Thị', readonly=True , compute='_compute_display_name', store=False)
    birth_date = fields.Date(string='Ngày Sinh')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Số Điện Thoại')
    book_id = fields.One2many("library.book", "student_id")
    books_count = fields.Integer(string="Sách đã mượn", compute="_compute_books_count")

    def _compute_books_count(self):
        for student in self:
            student.books_count = len(student.book_id)

    @api.depends('name', 'student_code')
    def _compute_display_name(self):
        for student in self:
            if student.name and student.student_code:
              student.display_name = f'{student.name}-{student.student_code}'
            else:
              student.display_name = ''

    @api.constrains('birth_date')
    def _check_birth_date(self):
        for record in self:
            if record.birth_date:
                if record.birth_date > date.today():
                    raise ValidationError("Ngày sinh không thể sau ngày hiện tại.")

    @api.constrains('student_code')
    def _check_unique_student_id(self):
        for record in self:
            if self.search_count([('student_code', '=', record.student_code)]) > 1:
                raise ValidationError("Mã sinh viên đã tồn tại, vui lòng nhập mã sinh viên khác!")

    def action_view_partners(self):
        partner_id = self.env['res.partner'].search([
            ('student_ids', '=', self.id),
            ('is_student', '=', True)
        ])
        if partner_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Partners',
                'res_model': 'res.partner',
                'view_mode': 'tree',
                'domain': [('id', '=', partner_id.id)],
                'target': 'current',
            }
        else:
         raise UserError("Chưa liên kết với liên hệ nào, vui lòng vào liên hệ cập nhật")
