from odoo import models, fields, api



class DoodexPendaftaran(models.Model):
    _name = 'doodex.pendaftaran'
    _description = 'pendaftaran doodex'

    # id_pendaftaran = fields.Char(string='ID Pendaftaran')
    # nama = fields.Char(string='Nama Pasien')
    # no_hp = fields.Integer(string='No HP')
    # alamat = fields.Text(string='Alamat')
    # umur = fields.Integer(string='Umur')
    # tgl_pendaftaran = fields.Date(string='Tanggal Pendaftaran')
    # state = fields.Selection(string='Status', 
    #                          selection=[('new', 'New'), 
    #                                     ('in_progress', 'In Progress'),
    #                                     ('completed', 'Completed'),])
    # keluhan = fields.Text(string='Keluhan Pasien')
    # pasien_id = fields.One2many(comodel_name='doodex.pasien', 
    #                             inverse_name= 'name_pasien',
    #                             string='Pasien')


    nama = fields.Char(string='Nama', required=True)
    no_hp = fields.Char(string='Nomor HP', required=True)
    alamat = fields.Text(string='Alamat')
    umur = fields.Integer(string='Umur')
    state = fields.Selection(string='Status',
                              selection=[('new', 'New'), 
                                         ('in_progress', 'In Progress'),
                                        ('completed', 'Completed'),])
    tgl_pendaftaran = fields.Date(string='Tanggal Pendaftaran', default=fields.Date.today())
    keluhan = fields.Text(string='Keluhan')

    
    # pasien = fields.One2many(comodel_name='doodex.pasien', 
    #                          inverse_name='nama_pasien', 
    #                          string='Pasien')
    # dokter = fields.Many2one(comodel_name='doodex.dokter', 
    #                          string='Dokter')
    # rekam_mediss = fields.One2many(comodel_name='doodex.rekam.medis', 
    #                                inverse_name='pendaftaran', 
    #                                string='Rekam Medis')