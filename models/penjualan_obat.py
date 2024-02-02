from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError



class DoodexPenjualanObat(models.Model):
    _name = 'doodex.penjualan.obat'
    _description = 'DoodexPenjualanObat'

    # name = fields.Char(string='')
    referensi_penjualan_obat = fields.Char(string='No. Reference Penjualan Obat',
                            required=True,
                            copy=False,
                            readonly=True,
                            default=lambda self: _('New'))
    name = fields.Char(string='Nama Pembeli')
    tgl_penjualan = fields.Datetime('Tanggal Transaksi',
                                    default = fields.Datetime.now())
    total_bayar = fields.Integer(compute='_compute_total_bayar', 
                              string='Total Pembayaran')
    detail_penjualan_obat_ids = fields.One2many(comodel_name='doodex.detail.penjualan.obat', 
                                          inverse_name='penjualan_id', 
                                          string='Detail Penjualan')
    petugas_apotek_id = fields.Many2one(comodel_name='doodex.petugas.apotek', 
                                        string='Petugas Apotek')
    state = fields.Selection(string='Status',
                            selection=[('draft','Draft'),
                                       ('confirm','Confirm'),
                                       ('done','Done'),
                                       ('cancel','Cancel')],
                            required=True, 
                            readonly=True, 
                            default='draft')
    
    def action_confirm(self):
        self.write({'state': 'confirm'})
    def action_done(self):
        self.write({'state': 'done'})
    def action_cancel(self):
        self.write({'state': 'cancel'})
    def action_draft(self):
        self.write({'state': 'draft'})
    
        
    @api.depends('detail_penjualan_obat_ids')
    def _compute_total_bayar(self):
        for rec in self:
            a = sum(self.env['doodex.detail.penjualan.obat'].search([('penjualan_id', '=', rec.id)]).mapped('subtotal'))
            rec.total_bayar = a

    @api.model
    def create(self,vals):
        if vals.get('referensi_penjualan_obat', _("New")) == _("New"):
            vals['referensi_penjualan_obat'] = self.env['ir.sequence'].next_by_code('referensi.penjualan.obat') or _("New")
        record = super(DoodexPenjualanObat, self).create(vals)
        return record
    
    def unlink(self):
        for record in self:
            if record.state in ('confirm', 'done'):
                raise ValidationError("You cannot delete a sent quotation or a confirmed sales order. You must first cancel it.")
        if self.detail_penjualan_obat_ids:
            a = []
            for detail in self:
                a = self.env['doodex.detail.penjualan.obat'].search([('penjualan_id', '=', detail.id)])
            for obat in a:
                obat.obat_id.stok += obat.qty
        return super(DoodexPenjualanObat, self).unlink()
    
    
    # create def write for penjualan and pembelian    
    def write(self,vals):
        for rec in self:
            a = self.env['doodex.detail.penjualan.obat'].search([('penjualan_id','=',rec.id)])
            print(a)
            for data in a:
                print(str(data.obat_id.name)+" "+str(data.qty))
                data.obat_id.stok += data.qty
        record = super(DoodexPenjualanObat, self).write(vals)
        for recc in self:
            b = self.env['doodex.detail.penjualan.obat'].search([('penjualan_id','=',recc.id)])
            for databaru in b:
                if databaru in a:
                    print(str(databaru.obat_id.name)+" "+str(databaru.qty))
                    databaru.obat_id.stok -= databaru.qty
        return record


class DoodexDetailPenjualanObat(models.Model):
    _name = 'doodex.detail.penjualan.obat'
    _description = 'DoodexDetailPenjualanObat'

    name = fields.Char(string='Nama')
    penjualan_id = fields.Many2one(comodel_name='doodex.penjualan.obat', 
                                   string='Detail Penjualan Obat')
    obat_id = fields.Many2one(comodel_name='doodex.obat', 
                              string='Daftar Obat')
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
        rec = super(DoodexDetailPenjualanObat, self).create(vals)
        if rec.qty:
            self.env['doodex.obat'].search([('id', '=', rec.obat_id.id)]).write({'stok' : rec.obat_id.stok - rec.qty})
        return rec
    
    @api.constrains('qty')
    def _check_qty(self):
        for rec in self:
            if rec.qty < 1:
                raise ValidationError('masa mau beli {} cuma {} pcs'
                                      .format(rec.obat_id.name, rec.qty))
            elif rec.qty > rec.obat_id.stok:
                raise ValidationError('jumlah {} yang ada melebihi dari yang anda minta (Stok: {})'
                                      .format(rec.obat_id.name, rec.obat_id.stok))
    
