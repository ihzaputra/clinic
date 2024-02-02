from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import ValidationError



class DoodexJanjiTemu(models.Model):
    _name = 'doodex.janji.temu'
    _description = 'doodex janji temu'

    referensi_janji_temu = fields.Char(string='No. Reference Janji Temu',
                            required=True,
                            copy=False,
                            readonly=True,
                            default=lambda self: _('New'))
    name = fields.Char(string='Nama Janji Temu')
    dokter = fields.Many2one(comodel_name='doodex.dokter', 
                             string='Dokter')
    pasien = fields.Many2one(comodel_name='doodex.pasien', 
                             string='Pasien')
    tgl_janji_temu = fields.Date(string='Tanggal Janji Temu')
    state = fields.Selection(string='Status', 
                             selection=[('draft', 'Draft'), 
                                        ('on progress', 'On Progress'),
                                        ('done', 'Done'),
                                        ('cancel', 'Cancel')],
                            required=True, 
                            readonly=True, 
                            default='draft')
    rekam_medis_id = fields.Many2one(comodel_name='doodex.rekam.medis', 
                                     string='Rekam Medis')
    layanan_id = fields.Many2one(comodel_name='doodex.layanan', 
                                 string='Layanan')
    harga = fields.Integer(string='Harga Layanan')

    @api.model
    def create(self,vals):
        if vals.get('referensi_janji_temu', _("New")) == _("New"):
            vals['referensi_janji_temu'] = self.env['ir.sequence'].next_by_code('referensi.janji.temu') or _("New")
        record = super(DoodexJanjiTemu, self).create(vals)
        return record
    
    def unlink(self):
        for record in self:
            if record.state in ('on progress', 'done'):
                raise ValidationError("You cannot delete a sent quotation or a confirmed sales order. You must first cancel it.")
    
    
    @api.onchange('layanan_id')
    def onchange_layanan_id(self):
        if self.layanan_id:
            self.harga = self.layanan_id.harga_layanan

    def action_on_progress(self):
        self.write({'state': 'on progress'})
    def action_done(self):
        self.write({'state': 'done'})
    def action_cancel(self):
        self.write({'state': 'cancel'})
    def action_draft(self):
        self.write({'state': 'draft'})
    



    @api.constrains('tgl_janji_temu', 'dokter', 'state')
    def _check_appointment_constraints(self):
        for janji_temu in self:
            if janji_temu.state == 'on progress':
                duplicate_appointments = self.env['doodex.janji.temu'].search([
                    ('tgl_janji_temu', '=', janji_temu.tgl_janji_temu),
                    ('dokter', '=', janji_temu.dokter.name),
                    ('state', '=', 'on progress'),
                    ('id', '!=', janji_temu.id),
                ])
                if duplicate_appointments:
                    raise ValidationError('Satu dokter hanya bisa memiliki satu pertemuan "on progress" pada hari yang sama.')

            if janji_temu.state in ['done', 'on progress']:
                done_appointments = self.env['doodex.janji.temu'].search([
                    ('tgl_janji_temu', '=', janji_temu.tgl_janji_temu),
                    ('dokter', '=', janji_temu.dokter.id),
                    ('state', '=', 'done'),
                ])

                on_progress_appointments = self.env['doodex.janji.temu'].search([
                    ('tgl_janji_temu', '=', janji_temu.tgl_janji_temu),
                    ('dokter', '=', janji_temu.dokter.id),
                    ('state', '=', 'on progress'),
                ])

                total_appointments = len(done_appointments) + len(on_progress_appointments)

                if total_appointments >= 6:
                    raise ValidationError('Maksimal 5 pertemuan per hari untuk satu dokter.')
            
            if janji_temu.tgl_janji_temu and janji_temu.tgl_janji_temu < fields.Date.today():
                raise ValidationError('Tanggal janji temu tidak boleh kurang dari hari ini.')
                