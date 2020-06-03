from odoo.tests.common import TransactionCase

class TestTask(TransactionCase):

    def setUp(self, *args, **kwargs):
        result = super().setUp(*args, **kwargs) 
        #Need to check access security p.84
            #This is for user
        #user_admin = self.env.ref('base.user_admin') 
        #self.env= self.env(user=user_admin)
            #This is for manager
        #
        #
        
        
        self.Task = self.env['task_management_task'] 
        self.task_ode = self.Task.create(
                { 'name': 'CMPT Assignment', 
                  'assignee': 'Haosen'}) 
        return result 
        
    def test_create(self):
        self.assertEqual(self.task_ode.finished, False)
    
    #Need to check due day is not before today
    
    