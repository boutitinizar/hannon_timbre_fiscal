from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class HnConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    hn_enable_tax = fields.Boolean(string="Timbre Fiscal")
    hn_amount_tax = fields.Monetary(string="Montant")
    hn_sales_tax_account = fields.Many2one('account.account', string="TF Vente")
    hn_purchase_tax_account = fields.Many2one('account.account', string="TF Achat")

    def get_values(self):
        ks_res = super(HnConfigSettings, self).get_values()
        ks_res.update(
            hn_enable_tax=self.env['ir.config_parameter'].sudo().get_param('hn_enable_tax'),
            hn_sales_tax_account=int(self.env['ir.config_parameter'].sudo().get_param('hn_sales_tax_account')),
            hn_purchase_tax_account=int(self.env['ir.config_parameter'].sudo().get_param('hn_purchase_tax_account')),
            hn_amount_tax=float(self.env['ir.config_parameter'].sudo().get_param('hn_amount_tax')),
        )
        return ks_res

    def set_values(self):
        super(HnConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('hn_enable_tax', self.hn_enable_tax)
        if self.hn_enable_tax:
            self.env['ir.config_parameter'].set_param('hn_amount_tax', self.hn_amount_tax)
            self.env['ir.config_parameter'].set_param('hn_sales_tax_account', self.hn_sales_tax_account.id)
            self.env['ir.config_parameter'].set_param('hn_purchase_tax_account', self.hn_purchase_tax_account.id)
