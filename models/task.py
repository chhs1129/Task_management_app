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
    assignee_id = fields.Many2one('res.users', string = 'Assigned to', required = True)
    #Task category
    category_id = fields.Many2one('task_management_category', string='category')
    #Task Coordinators
    coordinator_ids = fields.Many2many('res.users', string = 'coordinators', required = False)
    #Assiged by whom?
    assigned_by = fields.Many2one('res.users', string = 'Assigned by', default=lambda self: self.env.user)
    
    #State
    state = fields.Selection(
        [('new','Draft'),
         ('open','Assigned'),
         ('done','Finished'),
         ('cancel', 'Closed')],
        default='new',
    )

    #Is Task overtime?
    overtime = fields.Boolean('Task Overtime?', compute='_check_if_overtime',store=True)
    #Is current user a coordinator?
    current_user_group = fields.Char('Current user group',compute='_dynamic_get_group')
    
    
    
    
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
    def is_coordinator(self):
        self.ensure_one()
        for rec in self.coordinator_ids:
            if rec  ==  self.env.user:
                return True
            return False
        
    @api.multi
    def write(self, values):
        if self.env['res.users'].has_group('task_management_app.task_group_manager') != True and self.is_coordinator() == False:
                raise UserError( 'Task must be edited by the manager or coordinator.')
        if self.state != 'open' and self.state !='done':
            return super(Task, self).write(values)
        else:
                raise UserError('You cannot approve the task at this current state.')
    
    @api.depends('due_date')
    @api.multi
    def _check_if_overtime(self):
        for record in self:
            '''
            if record.coordinator_ids  ==  self.env.user:
                record.current_user_group = True
            else:
                record.current_user_group = False
            print(record.current_user_group)
            '''
            record.overtime = record.due_date < fields.Datetime.now()
    
    @api.depends('current_user_group')
    @api.multi
    def _dynamic_get_group(self):
        for record in self:
            if record.env['res.users'].has_group('task_management_app.task_group_manager') == True:
                record.current_user_group = 'manager' 
            else:
                record.current_user_group = 'user'
                for rec in record.coordinator_ids:
                        if record.env.user == rec:
                            record.current_user_group = 'coordinator'

                

    def button_submit(self):
        super(Task, self).write({'state':'done'})
        '''
        self.submitted = True
        self.state = 'done'
        '''
        
    @api.multi
    def button_approve(self):
        if self.state == 'done' and self.current_user_group != 'user':

            super(Task, self).write({'state':'cancel'})
            '''
            self.finished = True
            self.state = 'cancel'
            '''
            
    def button_reject(self):
        if self.state == 'done' and self.current_user_group != 'user':
            super(Task, self).write({'state':'new'})        
            
    @api.multi
    def action_approve(self):
        for record in self:
            if record.current_user_group == 'user':
                raise UserError('As a User, you cannot approve a task.')
            if record.state == 'done' and self.current_user_group != 'user':
                super(Task, record).write({'state':'cancel'})
    
    
    
    
