from odoo import models, fields, api



class DoodexLayanan(models.Model):
    _name = 'doodex.layanan'
    _description = 'doodex layanan'

    name = fields.Selection(string='Layanan', 
                               selection=[('konsultasi umum', 'Konsultasi Umum'), 
                                          ('pemeriksaan mata', 'Pemeriksaan Mata'),
                                          ('pemeriksaan gigi', 'Pemeriksaan Gigi'),])
    harga_layanan = fields.Integer(string='Harga Layanan')
    
    @api.onchange('name', 'harga_layanan')
    def _onchange_harga_layanan(self):
        if self.name == 'konsultasi umum':
            self.harga_layanan = 50000
        elif self.name == 'pemeriksaan mata':
            self.harga_layanan = 40000
        elif self.name == 'pemeriksaan gigi':
            self.harga_layanan = 30000
