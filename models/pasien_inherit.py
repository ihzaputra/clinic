from odoo import models, fields, api



class DoodexPasienInherit(models.Model):
    _inherit = 'res.partner'

    id_pasien = fields.Char(string='ID Pasien')
    nama_pasien = fields.Char(string='Nama Pasien')
    gender_pasien = fields.Selection(string='Jenis Kelamin Pasien', 
                                     selection=[('male', 'Male'), 
                                                ('female', 'Female'),])
    no_hp = fields.Integer(string='No Hp Pasien')
    umur_pasien = fields.Integer(string='Umur Pasien')
    alamat_pasien = fields.Text(string='Alamat Pasien')
    riwayat_penyakit = fields.Text(string='Riwayat Penyakit')
    