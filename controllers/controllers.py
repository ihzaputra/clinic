# -*- coding: utf-8 -*-
# from odoo import http


# class ClinicDoodex(http.Controller):
#     @http.route('/clinic_doodex/clinic_doodex', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/clinic_doodex/clinic_doodex/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('clinic_doodex.listing', {
#             'root': '/clinic_doodex/clinic_doodex',
#             'objects': http.request.env['clinic_doodex.clinic_doodex'].search([]),
#         })

#     @http.route('/clinic_doodex/clinic_doodex/objects/<model("clinic_doodex.clinic_doodex"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('clinic_doodex.object', {
#             'object': obj
#         })
