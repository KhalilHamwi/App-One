from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    property_id = fields.Many2one('property')
    owner_id = fields.Many2one('owner')
    owner_name_property = fields.Char(compute='_compute_name', string='Owner')

    @api.depends('property_id')
    def _compute_name(self):
        for rec in self:
            rec.owner_name_property = rec.property_id.owner_id.name

    # def action_confirm(self):
    #     res = super(SaleOrder, self).action_confirm()
    #
    #     # Update the active and state fields of the associated property record
    #     if self.property_id:
    #         self.property_id.active = False
    #         self.property_id.state = 'closed'
    #     return res
    #
    # def action_cancel(self):
    #     res = super(SaleOrder, self).action_confirm()
    #     if self.property_id:
    #         self.property_id.active = True
    #         self.property_id.state = 'draft'
    #
    #     return res
