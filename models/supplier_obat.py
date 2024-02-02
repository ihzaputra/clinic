from odoo import models, fields, api


class DoodexSupplierObat(models.Model):
    _name = 'doodex.supplier.obat'
    _description = 'doodex supplier obat'

    name = fields.Char(string='Nama Supplier Obat')
    phone = fields.Char(string='No. Telepon')
    cp = fields.Char(string='Contact Person')
    alamat = fields.Char(string='Alamat')
    obat_ids = fields.Many2many(comodel_name='doodex.obat', 
                                string='Supply Obat')
    
    