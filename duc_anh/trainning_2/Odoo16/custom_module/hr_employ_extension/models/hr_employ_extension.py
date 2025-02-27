from pkg_resources import require

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    years_of_experience = fields.Integer(string="Years of Experience", compute="_compute_years_of_experience",
                                         store=True, readonly=True)

    certifications = fields.One2many('employee.certification', 'employee_id', string="Certifications")

    skills = fields.One2many('employee.skill', 'employee_id', string="Skills")

    has_certifications = fields.Boolean(compute='_compute_has_certifications', string="Has Certifications", store=False)

    @api.depends('certifications')
    def _compute_has_certifications(self):
        for employee in self:
            employee.has_certifications = bool(employee.certifications)

    @api.depends('certifications.years_of_experience', 'skills.years_of_experience')
    def _compute_years_of_experience(self):
        for record in self:
            if len(record.certifications) > 0:
                total_experience = 0
                for cert in record.certifications:
                    total_experience += cert.years_of_experience
                for skill in record.skills:
                    total_experience += skill.years_of_experience
                record.years_of_experience = total_experience
            else:
                record.years_of_experience = 0

    def action_open_certification_skill_wizard(self):
        if not self.has_certifications:
            raise ValidationError("Employee hiên tại không có bất kỳ chứng chỉ nào để cập nhật")
        return {
            'name': 'Update Skills',
            'type': 'ir.actions.act_window',
            'res_model': 'employee.skill.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_employee_id': self.id,
            },
        }

class EmployeeCertification(models.Model):
    _name = 'employee.certification'
    _sql_constraints = [
        ('name_unique', 'unique(employee_id, name)', 'Certification name must be unique for each employee.')
    ]

    employee_id = fields.Many2one('hr.employee', string="Employee")
    skill_id = fields.One2many('employee.skill', 'certification_id', string="Skills")
    name = fields.Char(string="Certification Name", required=True)
    date_issued = fields.Date(string="Date Issued")
    years_of_experience = fields.Integer(string="Years of Experience", required=True)

    @api.constrains('years_of_experience')
    def _check_years_of_experience(self):
        for employee in self:
            if employee.years_of_experience <= 0:
                raise ValidationError("Số năm kinh nghiệm phải lớn hơn 0")

    @api.constrains('date_issued')
    def _check_date_issued(self):
        for employee in self:
            if employee.date_issued > fields.Date.today():
                raise ValidationError("Ngày cấp phải nhỏ hơn hoặc bằng ngày hiện tại")

    def unlink(self):
        for record in self:
            print(record.skill_id, "record")
            if record.skill_id:
                self.env['employee.skill'].search([('certification_id', '=', record.id)]).unlink()
        return super(EmployeeCertification, self).unlink()

class EmployeeSkill(models.Model):
    _name = 'employee.skill'
    employee_id = fields.Many2one('hr.employee', string="Employee")
    certification_id = fields.Many2one('employee.certification', string="Certification")

    name = fields.Char(string="Skill Name", required=True)
    experience_points = fields.Integer(string="Experience Points")
    years_of_experience = fields.Integer(string="Years of Experience", required=True)

    @api.constrains('experience_points')
    def _check_experience_points(self):
        for employee in self:
            if employee.experience_points < 0:
                raise ValidationError("Điểm kinh nghiệm phải lớn hơn hoặc bằng 0")
            if employee.experience_points > 10:
                raise ValidationError("Điểm kinh nghiệm phải nhỏ hơn hoặc bằng 10")

    @api.constrains('years_of_experience')
    def _check_years_of_experience(self):
        for employee in self:
            if employee.years_of_experience < 0:
                raise ValidationError("Số năm kinh nghiệm phải lớn hơn hoặc bằng 0")

    @api.constrains('employee_id', 'certification_id')
    def _check_unique_employee_certification(self):
        for record in self:
            existing_record = self.env['employee.skill'].search([
                ('employee_id', '=', record.employee_id.id),
                ('certification_id', '=', record.certification_id.id)
            ])
            if existing_record and existing_record != record:
                raise ValidationError("Kỹ năng đi kèm chứng chỉ đã tồn tại")

    def create(self, vals_list):
        employee_ids = []
        print(vals_list)
        if isinstance(vals_list, list):
            employee_ids = list(set([vals.get('employee_id') for vals in vals_list if vals.get('employee_id')]))

        elif isinstance(vals_list, dict):
            employee_ids = [vals_list.get('employee_id')]

        for employee_id in employee_ids:
            skill_count = self.env['employee.skill'].search_count([('employee_id', '=', employee_id)])
            if skill_count >= 10:
                raise ValidationError("Nhân viên không thể có quá 10 kỹ năng")

        return super(EmployeeSkill, self).create(vals_list)

