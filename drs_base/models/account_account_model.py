from odoo import api, models


class AccountAccount(models.Model):
    _inherit = "account.account"

    @api.model_create_multi
    def create(self, data_list):
        for data in data_list:
            print(data.get("code"))
        return super().create(data_list)
