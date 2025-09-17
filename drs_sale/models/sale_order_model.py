from datetime import datetime, timedelta

from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    version_number = fields.Integer(default=lambda s: 1, copy=False)
    version_cluster = fields.Many2one(comodel_name="sale.order")

    @api.model
    def create(self, vals):
        order = super(SaleOrder, self).create(vals)
        if not self.env.context.get("avoid_cluster_copy", False):
            order.write(
                {
                    "version_cluster": order.id,
                    "name": f"{order.name}{order.version_number}",
                }
            )
        return order

    def new_version(self):
        # Recompute Dates
        d1 = self.date_order.date()
        d2 = self.validity_date
        self.with_context(avoid_cluster_copy=True).copy(
            {
                "version_number": self.version_number + 1,
                "version_cluster": self.version_cluster.id,
                "name": self.version_cluster.name[:-1] + f"{self.version_number + 1}",
                "validity_date": datetime.now() + timedelta(days=(d2 - d1).days),
            }
        )
        self.action_cancel()
        order_ids = [
            data["id"]
            for data in self.search_read(
                [("version_cluster", "in", self.version_cluster.ids)], ["id"]
            )
        ]
        return {
            "name": "Historial de versiones",
            "view_type": "form",
            "view_mode": "tree,form",
            "res_model": "sale.order",
            "type": "ir.actions.act_window",
            "target": "current",
            "domain": [("id", "in", order_ids)],
        }
