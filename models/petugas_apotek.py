from odoo import api, fields, models, _



class DoodexPetugasApotek(models.Model):
    _name = 'doodex.petugas.apotek'
    _description = 'New Description'

    id_petugas_apotek = fields.Char(string='ID Petugas Apotek',
                            required=True,
                            copy=False,
                            readonly=True,
                            default=lambda self: _('New'))
    name = fields.Char(string='Nama')
    alamat = fields.Char(string='Alamat')
    jenis_kelamin = fields.Selection([('Laki-laki','Laki-laki'),
                                      ('Perempuan','Perempuan')], 
                                      string='Jenis Kelamin')
    tgl_lahir = fields.Date(string='Tanggal Lahir')

    @api.model
    def create(self,vals):
        if vals.get('id_petugas_apotek', _("New")) == _("New"):
            vals['id_petugas_apotek'] = self.env['ir.sequence'].next_by_code('referensi.petugas.apotek') or _("New")
        record = super(DoodexPetugasApotek, self).create(vals)
        return record