from odoo import api, fields, models

class DoodexJenisObat(models.Model):
     _name = 'doodex.jenis.obat'
     _description = 'New Description'

     name = fields.Selection([('Obat Antibiotik', 'Obat Antibiotik'), 
                            ('Obat Cair', 'Obat Cair'), 
                            ('Obat Tablet/Kapsul','Obat Tablet/Kapsul'), 
                            ('Obat Oles','Obat Oles'),
                            ('Obat Tetes','Obat Tetes'),
                            ('Alat Medis','Alat Medis')], 
                            string='Jenis Obat') 
    
     kode_jenis = fields.Char(onchange='_compute_field_name', 
                              string='Kode Jenis Obat')
     
     letak = fields.Char(string='Nomor Rak')
     obat_ids = fields.One2many(comodel_name='doodex.obat', 
                                  inverse_name='jenis_obat_id', 
                                  string='Daftar Obat')
     jumlah_obat = fields.Char(compute='_compute_jumlah_obat', string='Jumlah Item')
    
    # UNTUK MENETAPKAN JENIS DAN LETAK OBAT
     @api.onchange('name')
     def _compute_kode_jenis(self):
        if (self.name =='Obat Antibiotik'):
            self.kode_jenis = 'antibiotik'
            self.letak = 1
        elif (self.name == 'Obat Cair'):
            self.kode_jenis = 'obatcair'
            self.letak = 2
        elif (self.name == 'Obat Tablet/Kapsul'):
            self.kode_jenis = 'tablet/kapsul' 
            self.letak = 3
        elif (self.name == 'Obat Oles'):
            self.kode_jenis = 'obatoles' 
            self.letak = 4
        elif (self.name == 'Obat Tetes'):
            self.kode_jenis = 'obattetes'
            self.letak = 5
        elif (self.name == 'Alat Medis'):
            self.kode_jenis = 'alatmedis'
            self.letak = 6 

    
     @api.depends('obat_ids')
     def _compute_jumlah_obat(self):
        for rec in self:
            a = self.env['doodex.obat'].search([('jenis_obat_id','=', rec.id)]).mapped('name')
            b = len(a)
            rec.jumlah_obat = b
            # rec.daftar = a

    #  daftar = fields.Char(string='Daftar Isi')