from odoo import models, fields, api, _



class DoodexDokter(models.Model):
    _name = 'doodex.dokter'
    _description = 'dokter doodex'
    _rec_name = 'name'

    id_dokter = fields.Char(string='ID Dokter',
                            required=True,
                            copy=False,
                            readonly=True,
                            default=lambda self: _('New'))
    name = fields.Char(string='Nama')
    jenis_kelamin = fields.Selection(string='Jenis Kelamin Dokter', 
                                     selection=[('male', 'Male'), 
                                                ('female', 'Female'),])
    spesialisasi = fields.Selection(string='Spesialisasi Dokter',
                                    selection=[('Dokter Anak','Dokter Anak'),
                                               ('Dokter Umum','Dokter Umum'),
                                               ('Dokter THT','Dokter THT'),
                                               ('Dokter Mata','Dokter Mata'),
                                               ('Dokter Gigi','Dokter Gigi'),
                                               ('Dokter Kulit','Dokter Kulit')])
    alamat = fields.Char(string='Alamat')
    tgl_lahir = fields.Date(string='Tanggal Lahir')
    gambar = fields.Image('Gambar')
    
    @api.model
    def create(self,vals):
        if vals.get('id_dokter', _("New")) == _("New"):
            vals['id_dokter'] = self.env['ir.sequence'].next_by_code('referensi.dokter') or _("New")
        record = super(DoodexDokter, self).create(vals)
        return record

# KITA BISA DEFINE WAKTU AVAILABILITY DARI DOKTER DAN NANTI SISA DI BIKIN LOGIC YANG JIKA DATETIME.NOW > DEFINE TERSEBUT MAKA DOKTER TERSEBUT TIDAK AVAILABLE