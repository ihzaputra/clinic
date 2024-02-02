from io import BytesIO
from odoo import models, fields, api, _
try:
    import qrcode
except ImportError:
    qrcode = None
try:
    import base64
except ImportError:
    base64 = None


class DoodexRekamMedis(models.Model):
    _name = 'doodex.rekam.medis'
    _description = 'rekam medis doodex'

    no_antrian = fields.Char(string='No Antrian')
    name = fields.Many2one(comodel_name='doodex.pasien', 
                           string='Nama Pasien')
    jenis_kelamin = fields.Selection([('laki-laki', 'Laki-laki'),
                                    ('perempuan', 'Perempuan')], 
                                    string='Jenis Kelamin')
    umur = fields.Char(string='Umur')
    tinggi = fields.Char(string='Tinggi Badan')
    berat = fields.Char(string='Berat Badan')
    keluhan = fields.Selection([('Asma','Asma'),
                                ('Maag','Maag'),
                                ('Alergi','Alergi'),
                                ('Sakit Kepala','Sakit Kepala'),
                                ('Darah Tinggi','Darah Tinggi'),
                                ('Penyakit Jantung','Penyakit Jantung'),
                                ('Flu dan Sakit Tenggorokan','Flu dan Sakit Tenggorokan')
                                ], string='Keluhan & Riwayat Penyakit')
    dokter_id = fields.Many2one(comodel_name='doodex.dokter', 
                                string='Dokter')
    total_bayar = fields.Integer(compute='_compute_total_bayar', 
                              string='Total Pembayaran')
    detail_rekam_medis_ids = fields.One2many(comodel_name='doodex.detail.rekam.medis', 
                                          inverse_name='rekam_medis_id', 
                                          string='Detail Penjualan')
    janji_temu_ids = fields.One2many(comodel_name='doodex.detail.janji.temu', 
                                  inverse_name='rekam_medisss', 
                                  string='Janji Temu')
    total_bayar_layanan = fields.Integer(compute='_compute_total_bayar_layanan',
                                         string='Total Pembayaran Layanan')
    total_bayar_administrasi = fields.Integer(compute='_compute_total_bayar_administrasi',
                                              string='Total Pembayaran Administrasi')
    qr_code_rekam_medis = fields.Char(compute='_compute_qr_code_rekam_medis', 
                                    string='QR Code Rekam Medis',
                                    store=True)
    
    @api.depends('no_antrian')
    def _compute_qr_code_rekam_medis(self):
        for rec in self:
            if qrcode and base64:
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3, border=4)
                qr.add_data(rec.no_antrian)
                qr.make(fit=True)
                img = qr.make_image()
                temp = BytesIO()
                img.save(temp, format='PNG')
                qr_image = base64.b64encode(temp.getvalue())
                rec.update({'qr_code_rekam_medis': qr_image})


    @api.depends('janji_temu_ids')
    def _compute_total_bayar_layanan(self):
        for rec in self:
            total_layanan = sum(rec.janji_temu_ids.mapped('harga'))
            rec.total_bayar_layanan = total_layanan

    @api.depends('total_bayar', 'total_bayar_layanan')
    def _compute_total_bayar_administrasi(self):
        for rec in self:
            rec.total_bayar_administrasi = rec.total_bayar + rec.total_bayar_layanan

    @api.depends('detail_rekam_medis_ids')
    def _compute_total_bayar(self):
        for rec in self:
            a = sum(self.env['doodex.detail.rekam.medis'].search([('rekam_medis_id', '=', rec.id)]).mapped('subtotal'))
            rec.total_bayar = a
    
    @api.onchange('name')
    def onchange_name(self):
        if (self.name):
            self.umur = self.name.umur
            self.jenis_kelamin = self.name.jenis_kelamin
            self.tinggi = self.name.tinggi
            self.berat = self.name.berat
            self.no_antrian = self.name.no_antrian
    
    

class DoodexDetailResep(models.Model):
    _name = 'doodex.detail.rekam.medis'
    _description = 'DoodexDetailRekamMedis'
    _rec_name = 'name'

    name = fields.Char(string='Nama')
    rekam_medis_id = fields.Many2one(comodel_name='doodex.rekam.medis', 
                                     string='Detail Rekam Medis')
    obat_id = fields.Many2one(comodel_name='doodex.obat', 
                                string='Obat')
    harga_satuan = fields.Integer(string='Harga Satuan')
    qty = fields.Integer(string='Quantity')
    subtotal = fields.Integer(compute='_compute_subtotal', 
                           string='Subtotal')

    # MENGHITUNG TOTAL
    @api.depends('harga_satuan', 'qty')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.qty * rec.harga_satuan
    
    @api.onchange('obat_id')
    def onchange_obat_id(self):
        self.harga_satuan = self.obat_id.harga_jual
    
    @api.model
    def create(self, vals):
        rec = super(DoodexDetailResep, self).create(vals)
        if rec.qty:
            self.env['doodex.obat'].search([('id', '=', rec.obat_id.id)]).write({'stok' : rec.obat_id.stok - rec.qty})
        return rec



class DoodexDetailJanjiTemu(models.Model):
    _name = 'doodex.detail.janji.temu'
    _description = 'DoodexDetailJanjiTemu'
    _rec_name = 'name'

    name = fields.Char(string='Nama')
    rekam_medisss = fields.Many2one(comodel_name='doodex.rekam.medis', 
                                    string='Rekam Medis')
    janji_temu_id = fields.Many2one(comodel_name='doodex.janji.temu', 
                                    string='Janji Temu')
    dokter = fields.Many2one(comodel_name='doodex.dokter', 
                             string='Dokter')
    pasien = fields.Many2one(comodel_name='doodex.pasien', 
                             string='Pasien')
    tgl_janji_temu = fields.Date(string='Tanggal Janji Temu')
    harga = fields.Integer(string='Harga Layanan')

    
    @api.onchange('janji_temu_id')
    def onchange_janji_temu_id(self):
        if (self.janji_temu_id):
            self.name = self.janji_temu_id.name
            self.dokter = self.janji_temu_id.dokter
            self.pasien = self.janji_temu_id.pasien
            self.tgl_janji_temu = self.janji_temu_id.tgl_janji_temu
            self.harga = self.janji_temu_id.harga
    
    
            