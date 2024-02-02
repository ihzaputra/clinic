from odoo import api, fields, models, _



class DoodexPerawat(models.Model):
    _name = 'doodex.perawat'
    _description = 'New Description'

    id_perawat = fields.Char(string='ID Perawat',
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
        if vals.get('id_perawat', _("New")) == _("New"):
            vals['id_perawat'] = self.env['ir.sequence'].next_by_code('referensi.perawat') or _("New")
        record = super(DoodexPerawat, self).create(vals)
        return record