# -*- coding: utf-8 -*-
from odoo import http

# class TaskManagementSystem(http.Controller):
#     @http.route('/task_management_system/task_management_system/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/task_management_system/task_management_system/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('task_management_system.listing', {
#             'root': '/task_management_system/task_management_system',
#             'objects': http.request.env['task_management_system.task_management_system'].search([]),
#         })

#     @http.route('/task_management_system/task_management_system/objects/<model("task_management_system.task_management_system"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('task_management_system.object', {
#             'object': obj
#         })