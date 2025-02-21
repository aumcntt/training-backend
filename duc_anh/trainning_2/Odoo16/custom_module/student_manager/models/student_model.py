from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Student(models.Model):
    _name = 'student.student'
    _description = 'Student Information'

    name = fields.Char(string='Tên Sinh Viên', required=True)
    student_code = fields.Char(string='Mã Sinh Viên', required=True)
    display_name = fields.Char(string='Tên Hiển Thị', readonly=True , compute='_compute_display_name', store=False)
    birth_date = fields.Date(string='Ngày Sinh')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Số Điện Thoại')

    @api.depends('name', 'student_code')
    def _compute_display_name(self):
        for student in self:
            if student.name and student.student_code:
              student.display_name = f'{student.name}-{student.student_code}'
            else:
              student.display_name = ''

    @api.constrains('student_code')
    def _check_unique_student_id(self):
        for record in self:
            if self.search_count([('student_code', '=', record.student_code)]) > 1:
                raise ValidationError("Mã sinh viên đã tồn tại, vui lòng nhập mã sinh viên khác!")
