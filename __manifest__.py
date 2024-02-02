# -*- coding: utf-8 -*-
{
    'name': "clinic_doodex",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'productivity',
    'application' : True,
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'report_xlsx'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/referensi_pasien.xml',
        'data/referensi_pegawai.xml',
        'data/referensi_transaksi.xml',
        'data/referensi_janji_temu.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/menu.xml',
        # 'views/pendaftaran_view.xml',
        'views/pasien_view.xml',
        'views/dokter_view.xml',
        'views/perawat_view.xml',
        'views/petugas_apotek_view.xml',
        'views/petugas_kebersihan_view.xml',
        'views/rekam_medis_view.xml',
        # 'views/pembayaran_view.xml',
        'views/obat_view.xml',
        'views/jenis_obat_view.xml',
        'views/supplier_obat_view.xml',
        'views/penjualan_obat_view.xml',
        'views/pembelian_obat_view.xml',
        'views/layanan_view.xml',
        'views/janji_temu_view.xml',
        'report/report.xml',
        'report/report_rekam_medis.xml',
        'report/report_pembelian_obat.xml',
        'report/report_penjualan_obat.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
