from odoo import models, fields, api

from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    # This Description For Name Model
    _description = 'Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=1)
    description = fields.Text()
    postcode = fields.Char(required=1)
    date_availability = fields.Date(tracking=1)
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute="_compute_diff")
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    active = fields.Boolean(default=True)
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('North', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    owner_id = fields.Many2one('owner')
    owner_phone = fields.Char(related='owner_id.phone')
    owner_address = fields.Char(related='owner_id.address')
    tag_ids = fields.Many2many('tag')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ], default='draft')
    line_ids = fields.One2many('property.line', 'property_id')

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name is exist!!')
    ]

    @api.depends('expected_price', 'selling_price', 'owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            print("inside _compute_diff methode")
            rec.diff = rec.expected_price - rec.selling_price

    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            print("inside _onchange_expected_price methode")
            return {
                'warning': {'title': 'warning', 'message': 'negative number', 'type': 'notification'}
            }

    @api.constrains('bedrooms')
    def check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError('Pleas Add Number For Bedrooms')

    def action_draft(self):
        for rec in self:
            print("inside draft action")
            rec.state = "draft"
            # rec.write({
            #     'state': 'draft'
            # })

    def action_pending(self):
        for rec in self:
            print("inside pending action")
            rec.write({
                'state': 'pending'
            })

    def action_sold(self):
        for rec in self:
            print("inside sold action")
            rec.write({
                'state': 'sold'
            })

    def action_closed(self):
        for rec in self:
            print("inside sold action")
            rec.write({
                'state': 'closed'
            })

    def check_expected_selling_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True

    # for create
    @api.model_create_multi
    def create(self, vals):
        res = super(Property, self).create(vals)
        # print("inside create methode")
        return res

    # for read
    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        res = super(Property, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
        # print("inside search method")
        return res

    # for update
    def write(self, vals):
        res = super(Property, self).write(vals)
        # print("inside write methode")
        return res

    # for delete
    def unlink(self):
        res = super(Property, self).unlink()
        # print("inside unlink method")
        return res


class PropertyLine(models.Model):
    _name = 'property.line'

    property_id = fields.Many2one('property')
    area = fields.Float()
    description = fields.Char()
