# -*- coding: utf-8 -*-

from odoo import models, fields, api 
from odoo.exceptions import UserError

class Task(models.Model):
    _name = 'task_management_task' 
    _description = 'Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    #Task Name
    name = fields.Char('Task Name', required = True) 
    #Task priority
    priority = fields.Selection([ ('normal', 'Normal'),('high', 'High'),],'Task Priority', default='normal',required = True)
    #Task due day
    due_date = fields.Datetime('Due date',required = True)
    #Task requirements (for manager)
    requirements = fields.Text('Task Requirements')
    #Task assignee
    assignee_id = fields.Many2one('res.users', string = 'Assignee', required = True)
    #Task category
    category_id = fields.Many2one('task_management_category', string='category')
    #State
    state = fields.Selection(
        [('new','Draft'),
         ('open','Assigned'),
         ('done','Finished'),
         ('cancel', 'Closed')],
        default='new',
    )
    #Is Task finished?
    finished = fields.Boolean('Finished?', default = False) 
    #Is Task overtime?
    overtime = fields.Boolean('Task Overtime?', compute='_check_if_overtime')
    #Is Task submitted to the manager?
    submitted = fields.Boolean('Task Submitted?', default = False)
    
    
    @api.model
    def create(self, values):
        # Override the original create function for the res.partner model
        record = super().create(values)
        # Change the values of a variable in this super function
        record.state = 'open'
        return record
    
    
    @api.multi
    def unlink(self):
        for record in self:
            if record.state != 'open' and record.state !='done':
                super(Task,record).unlink()
            else:    
                raise UserError( 'Cannot delete a in progress task.')

    @api.multi
    def write(self, values):
        if self.env['res.users'].has_group('task_management_app.task_group_manager') != True:
                raise UserError( 'Task must be edited by the manager.')
        if self.state != 'open' and self.state !='done':
            return super(Task, self).write(values)
        else:
                raise UserError('You cannot approve the task at this current state.')
    
    @api.depends('due_date','state')
    @api.multi
    def _check_if_overtime(self):
        for record in self:
                record.overtime = record.due_date < fields.Datetime.now()
       

    def button_submit(self):
        super(Task, self).write({'submitted':True})
        super(Task, self).write({'state':'done'})
        '''
        self.submitted = True
        self.state = 'done'
        '''
        
    @api.multi
    def button_approve(self):
        if self.submitted == True and self.env['res.users'].has_group('task_management_app.task_group_manager') == True:
            super(Task, self).write({'finished':True})
            super(Task, self).write({'state':'cancel'})
            '''
            self.finished = True
            self.state = 'cancel'
            '''
            
    def button_reject(self):
        if self.submitted == True and self.env['res.users'].has_group('task_management_app.task_group_manager') == True:
            super(Task, self).write({'submitted':False})
            super(Task, self).write({'state':'new'})        
            
    @api.multi
    def action_approve(self):
        for record in self:
            if record.env['res.users'].has_group('task_management_app.task_group_user') == True and record.env['res.users'].has_group('task_management_app.task_group_user')==False:
                raise UserError('You cannot approve a task.')
            if record.submitted == True and record.env['res.users'].has_group('task_management_app.task_group_manager') == True:
                super(Task, record).write({'finished':True})
                super(Task, record).write({'state':'cancel'})
    
    
    
    
