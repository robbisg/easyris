from qScience.model.user import User, Permission, Role
from mongoengine import connect
import itertools
import numpy as np

def run(database_config):
    
    from qScience.database.base import parse_db_config, easyris_connect
    
    db_config = parse_db_config(database_config)
    conn = easyris_connect(**db_config)
    
    actions = ['create', 'read', 'update', 'delete']

    actions_examination_status = ['start','go','stop','pause','finish','eject']
    actions_report_status = ['close', 'save', 'print', 'open']
    resources = [
                 'patient', 
                 'examination', 
                 'report',
                 'examination_status',
                 'report_status'
                ]
    
    permission_ = itertools.product(resources, actions)
    Permission.drop_collection()
    permission_list = []
    for it in permission_:
        p = Permission(it[1], it[0])
        p.save()
        permission_list.append(p)
        
        
    ex_status_permission = itertools.product(['examination'], actions_examination_status)
    for it in ex_status_permission:
        p = Permission(it[1], it[0])
        p.save()
        permission_list.append(p)
    
    
    report_status_permission = itertools.product(['report'], actions_report_status)
    for it in report_status_permission:
        p = Permission(it[1], it[0])
        p.save()
        permission_list.append(p)
    
    
    permission_dict = {'accettazione':np.array([1, 2, 3, 5, 6, 13, 14, 18, 30])-1,
                       'tecnico': np.array([2, 6, 7, 8, 14, 15, 16, 18, 21, 22, 23, 24, 25])-1,
                       'medico': np.array([2, 6, 9, 10, 11, 14, 17, 18, 19, 26, 27, 28, 29, 30])-1,
                       'amministrazione': np.array([2, 6, 10, 14, 18])-1,
                       'admin': np.arange(30)
                       }
    
    Role.drop_collection()
    for key_, value_ in permission_dict.iteritems():
        role_ = Role(key_, [permission_list[i] for i in value_])
        role_.save()
        
    User.drop_collection()
    role_medico = Role.objects(role_name='medico').first()

    user1 = User(username='mcaulo', 
                 password='massimo', 
                 roles=[role_medico],
                 first_name='Massimo',
                 last_name='Caulo',
                 telephone_number='3289876543',
                 mobile_number='3212345678',
                 email='mcaulo@unich.it')
    user1.save()
    
    
    role_acc = Role.objects(role_name='accettazione').first()
    user2 = User(username='gaetano', 
                 password='gaetano', 
                 roles=[role_acc],
                 first_name='Gaetano',
                 last_name='Di Gaetano',
                 telephone_number='3289876543',
                 mobile_number='3212345678',
                 email='gaetanodg@unich.it')
    user2.save()

    role_tecnico = Role.objects(role_name='tecnico').first()
    user3 = User(username='daniele', 
                 password='daniele', 
                 roles=[role_tecnico],
                 first_name='Daniele',
                 last_name='Petrucci',
                 telephone_number='3289876543',
                 mobile_number='3212345678',
                 email='danielepetrucci@unich.it')
    
    user3.save()
    
    role_amministrazione = Role.objects(role_name='amministrazione').first()
    user4 = User(username='michetti', 
                 password='michetti', 
                 roles=[role_amministrazione],
                 first_name='Carlo',
                 last_name='Michetti',
                 telephone_number='3289876543',
                 mobile_number='3212345678',
                 email='c.michetti@unich.it')
    
    user4.save()    
    
    role_admin = Role.objects(role_name='admin').first()
    user5 = User(username='chpiero', 
                 password='chpiero', 
                 roles=[role_admin],
                 first_name='Piero',
                 last_name='Chiacchiaretta',
                 telephone_number='3289876543',
                 mobile_number='3212345678',
                 email='p.chiacchiaretta@unich.it')
    
    user5.save() 
    
    user11 = User(username='valentina', 
                 password='valentina', 
                 roles=[role_medico],
                 first_name='Valentina',
                 last_name='Panara',
                 telephone_number='3289876543',
                 mobile_number='3212345678',
                 email='v.panara@unich.it')
    user11.save()

