from odoo import api, fields, models
from odoo.tools import html2plaintext


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    ctq_name = fields.Html(string="Descripción")

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if val.get("ctq_name"):
                val["name"] = html2plaintext(val["ctq_name"])
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("ctq_name"):
            vals["name"] = html2plaintext(vals["ctq_name"])
        return super().write(vals)

    @api.onchange("product_id")
    def _onchange_ctq_product(self):
        values = []
        if self.partner_id.lang:
            product = self.product_id.with_context(lang=self.partner_id.lang)
        else:
            product = self.product_id
        if not product:
            return False

        if product.partner_ref:
            values.append(product.partner_ref)
        if self.journal_id.type == "sale":
            if product.description_sale:
                values.append(product.description_sale)
        elif self.journal_id.type == "purchase":
            if product.description_purchase:
                values.append(product.description_purchase)
        ctq_name = "<p>" + "\n".join(values) if values else "" + "</p>"
        self.update({"ctq_name": ctq_name})
