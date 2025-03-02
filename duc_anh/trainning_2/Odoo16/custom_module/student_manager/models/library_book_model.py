from datetime import date

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    code = fields.Char(string='Mã sách', required=True, default=lambda self: self.env['ir.sequence'].next_by_code('library.book.sequence'))
    name = fields.Char(string='Tên sách', required=True)
    year = fields.Char(string='Năm xuất bản')
    author = fields.Char(string='Tác giả')
    student_id = fields.Many2one('student.student', string='Sinh viên')

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Mã sách phải là duy nhất!'),
    ]

    @api.constrains('year')
    def _check_year(self):
        for record in self:
            if record.year:
                try:
                    year = int(record.year)
                    if year <= 0:
                        raise ValidationError("Năm xuất bản phải lớn hơn 0.")
                    current_year = date.today().year
                    if year > current_year:
                        raise ValidationError(f"Năm xuất bản {year} không thể lớn hơn năm hiện tại {current_year}.")
                except ValueError:
                    raise ValidationError("Năm xuất bản không hợp lệ.")
