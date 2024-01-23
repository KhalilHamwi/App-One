from odoo import models, fields, api

from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_id = fields.Many2one('property')
    price = fields.Float(compute='_compute_price')
    owner_id = fields.Many2one('owner')
    owner_property = fields.Char(compute='_compute_owner')

    total_price = fields.Float(compute='_compute_total_price')

    @api.depends('property_id.selling_price')
    def _compute_price(self):
        for rec in self:
            rec.price = rec.property_id.selling_price

    @api.depends('owner_id.property_ids.name')
    def _compute_owner(self):
        for rec in self:
            rec.owner_property = ", ".join(rec.owner_id.property_ids.mapped('name'))

    @api.depends('owner_id.property_ids.name')
    def _compute_total_price(self):
        for rec in self:
            property_prices = rec.owner_id.property_ids.mapped('selling_price')
            if len(property_prices) >= 3:
                max_price = max(property_prices)
                total_sum = sum(property_prices) - max_price
                print('max_price:', max_price)
                print('total_sum:', total_sum)
                rec.total_price = max_price - total_sum
                if rec.total_price < 0:
                    rec.total_price = 1
                    return {
                        'warning': {'title': 'warning', 'message': 'negative number', 'type': 'notification'}
                    }
            else:
                if property_prices:
                    rec.total_price = max(property_prices) - min(property_prices)
                else:
                    rec.total_price = 1
    #                 for sum all property
    # rec.total_price = sum(rec.owner_id.property_ids.mapped('selling_price'))
