from odoo import models, fields, api


class EmployeeSkillWizard(models.TransientModel):
    _name = 'employee.skill.wizard'
    _description = 'Employee Skill Update Wizard'

    certification_id_list = []

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)

    certification_id = fields.Many2one(
        'employee.certification',
        string="Select Certification",
        domain="[('employee_id', '=', employee_id)]"
    )

    experience_points = fields.Integer(string="Experience Points", required=True)


    def action_update_skills(self):
        employee = self.employee_id
        certification = self.certification_id

        skill_name = f"Skill from {certification.name}"
        self.env['employee.skill'].create({
            'employee_id': employee.id,
            'name': skill_name,
            'experience_points' : self.experience_points,
            'certification_id': certification.id,
            'years_of_experience': 0
        })
        return {'type': 'ir.actions.act_window_close'}
