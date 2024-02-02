from odoo import models, fields, api



class DoodexObat(models.Model):
    _name = 'doodex.obat'
    _description = 'obat doodex'
    _rec_name = 'name'

    name = fields.Char(string='Nama Obat')
    harga_modal = fields.Integer(string='Harga Modal')
    harga_jual = fields.Integer(string='Harga Jual')
    stok = fields.Integer(string='Stok')
    gambar = fields.Image(string="Gambar")
    jenis_obat_id = fields.Many2one(comodel_name='doodex.jenis.obat',
                                    string='Jenis Obat')
    supplier_ids = fields.Many2many(comodel_name='doodex.supplier.obat', 
                                    string='Supplier')
    resep_ids = fields.Many2many(comodel_name='doodex.rekam.medis', 
                             string='Resep')
    
    
