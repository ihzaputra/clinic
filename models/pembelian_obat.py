from odoo import models, fields, api, _



class DoodexPembelian(models.Model):
    _name = 'doodex.pembelian.obat'
    _description = 'model.technical.name'

    
    obat_id = fields.Many2one(comodel_name='doodex.obat', 
                                string='Nama Barang')
    supplier_id = fields.Many2one(comodel_name='doodex.supplier.obat', 
                                  string='Supplier')
    qty_beli = fields.Integer(string='Quantiy Pembelian')
    modal = fields.Char(compute='_compute_modal', 
                        string='Harga Beli')
    bayar = fields.Char(compute='_compute_bayar', 
                        string='bayar')
    
    @api.depends('obat_id')
    def _compute_modal(self):
        for rec in self:
            rec.modal = rec.obat_id.harga_modal

    @api.depends('obat_id', 'qty_beli')
    def _compute_bayar(self):
        for rec in self:
            rec.bayar = rec.obat_id.harga_modal * rec.qty_beli
    
    
    @api.model
    def create(self,vals):           
        record = super(DoodexPembelian, self).create(vals)      
        if record.qty_beli: 
            self.env['doodex.obat'].search([('id','=',record.obat_id.id)]).write({'stok' : record.obat_id.stok + record.qty_beli})
        return record

    def unlink(self):
        for r in self:
            r.obat_id.stok -= r.qty_beli
        record = super(DoodexPembelian, self).unlink()
    
    @api.onchange('obat_id')
    def _onchange_obat(self):
        a = self.obat_id.supplier_ids
        b = []
        for i in a:            
            b.append(i.id)
        return {'domain':{'supplier_id':[('id','in',b)]}}

   
 