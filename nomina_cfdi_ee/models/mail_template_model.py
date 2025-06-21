import ast

from odoo import models


class MailTemplate(models.Model):
    _inherit = "mail.template"

    def _generate_template_attachments(self, res_ids, render_fields, render_results=None):
        self.ensure_one
        result = super()._generate_template_attachments(res_ids, render_fields, render_results)
        try:
            if self.env.ref("nomina_cfdi_ee.email_template_payroll", False).id == self.id:
                for res_id in res_ids:
                    slip = self.env["hr.payslip"].browse([res_id])
                    attachment = self.env["ir.attachment"].search(
                        [
                            ("res_id", "=", slip.id),
                            ("res_model", "=", slip._name),
                            ("name", '=', f"{slip.number.replace('/', '_')}.xml")
                        ]
                    )
                    result[res_id]["attachments"].append((attachment.name, attachment.raw))
        except (ValueError, KeyError, IndexError):
            pass
        return result
