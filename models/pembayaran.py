from odoo import models, fields, api



class DoodexPembayaran(models.Model):
    _name = 'doodex.pembayaran'
    _description = 'pembayaran doodex'

    id_pembayaran = fields.Char(string='ID Pembayaran')
    tgl_pembayaran = fields.Date(string='Tanggal Pembayaran')
    metode_pembayaran = fields.Selection(string='Metode Pembayaran', 
                                         selection=[('tunai', 'Tunai'), 
                                                    ('kartu_kredit', 'Kartu Kredit'),
                                                    ('transfer', 'Transfer'),])
    state = fields.Selection(string='Status', 
                             selection=[('belum_lunas', 'Belum Lunas'), 
                                        ('lunas', 'Lunas'),])
    # pendaftaran = fields.Many2many(comodel_name='doodex.pendaftaran', 
    #                                string='Pendaftaran')
    
