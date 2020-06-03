# -*- coding: utf-8 -*-
{
    'name': 'Task Management Application',

    'description': 'User can work on an assigned task and make reports to the manager',

    'application': True,
    
    'installable': True,
    
    'author': 'Haosen Cheng',

    'version': '0.1',

    'depends': ['base','mail'],

    'data': [
        'security/task_security.xml',
        'security/ir.model.access.csv',
        'security/ir.rule.xml',
        'views/task_view.xml',
        'views/category_view.xml',
        'views/task_menu.xml',
        'reports/task_report.xml'
    ],


}