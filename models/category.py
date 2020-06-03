# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Category(models.Model):
    _name = 'task_management_category' 
    _description = 'Task category' 
    
    #Category Name
    name = fields.Char('Category Name', required = True) 
    task_ids = fields.One2many('task_management_task', 'category_id', string='Task')
    count = fields.Integer('Number of Tasks', compute='_count_task_number')

    @api.depends('task_ids')
    @api.multi
    def _count_task_number(self):
        for record in self:
            record.count = len(record.task_ids)
    
    
    