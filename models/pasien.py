from odoo import models, fields, api, _



class DoodexPasien(models.Model):
    _name = 'doodex.pasien'
    _description = 'pasien doodex'
    
    no_antrian = fields.Char(string='No. Antrian',
                            required=True,
                            copy=False,
                            readonly=True,
                            default=lambda self: _('New'))
    name = fields.Char(string='Nama', required=True)
    jenis_kelamin = fields.Selection([('laki-laki', 'Laki-laki'),
                                    ('perempuan', 'Perempuan')], 
                                    string='Jenis Kelamin')
    tgl_lahir = fields.Date(string='Tanggal Lahir')
    umur = fields.Char(string='Umur')
    tinggi = fields.Char(string='Tinggi Badan')
    berat = fields.Char(string='Berat Badan')
    alamat = fields.Char(string='Alamat')
    
    @api.model
    def create(self,vals):
        if vals.get('no_antrian', _("New")) == _("New"):
            vals['no_antrian'] = self.env['ir.sequence'].next_by_code('referensi.pasien') or _("New")
        record = super(DoodexPasien, self).create(vals)
        return record
