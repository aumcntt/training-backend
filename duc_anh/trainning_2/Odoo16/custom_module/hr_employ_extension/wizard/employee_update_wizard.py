from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EmployeeUpdateWizard(models.TransientModel):
    _name = 'employee.update.wizard'
    _description = 'Wizard to update employee data'

    department_id = fields.Many2one('hr.department', string="Department")
    job_id = fields.Many2one('hr.job', string="Job Position")
    add_certification = fields.Many2one('employee.certification', string="Certification to Add")
    update_skills = fields.Char(string="Update Skills", compute="_compute_update_skills")
    add_experience_points = fields.Integer(string="Experience Points to Add", default=5)

    @api.depends('add_certification')
    def _compute_update_skills(self):
        for wizard in self:
            if wizard.add_certification:
                wizard.update_skills = f"Skill from {wizard.add_certification.name}"
            else:
                wizard.update_skills = ""

    @api.constrains('add_experience_points')
    def _check_add_experience_points(self):
        for record in self:
            if record.add_experience_points < 0:
                raise ValidationError("Điểm kinh nghiệm phải lớn hơn hoặc bằng 0")
            if record.add_experience_points > 10:
                raise ValidationError("Điểm kinh nghiệm phải nhỏ hơn hoặc bằng 10")

    @api.model
    def default_get(self, field):
        res = super(EmployeeUpdateWizard, self).default_get(field)
        return res

    def action_update_employees(self):
        employee_domain = [('employee_type', 'in', ['employee', 'freelancer'])]
        if self.department_id:
            employee_domain.append(('department_id', '=', self.department_id.id))
        if self.job_id:
            employee_domain.append(('job_id', '=', self.job_id.id))

        employees_to_update = self.env['hr.employee'].search(employee_domain)

        if not employees_to_update:
            raise ValidationError("Không tìm thấy nhân viên phù hợp")

        for employee in employees_to_update:
            if self.add_certification:
                employee.write({
                    'certifications': [(4, self.add_certification.id)]
                })

                skill_name = self.update_skills
                self.env['employee.skill'].create({
                    'employee_id': employee.id,
                    'name': skill_name,
                    'certification_id': self.add_certification.id,
                    'experience_points': self.add_experience_points,
                    'years_of_experience': 0
                })

        return {'type': 'ir.actions.act_window_close'}
