from odoo import api, fields, models, _



class DoodexPetugasKebersihan(models.Model):
    _name = 'doodex.petugas.kebersihan'
    _description = 'New Description'

    id_petugas_kebersihan = fields.Char(string='ID Petugas Kebersihan',
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
        if vals.get('id_petugas_kebersihan', _("New")) == _("New"):
            vals['id_petugas_kebersihan'] = self.env['ir.sequence'].next_by_code('referensi.petugas.kebersihan') or _("New")
        record = super(DoodexPetugasKebersihan, self).create(vals)
        return record