from easyris.user.model import User, Permission, Role
from mongoengine import connect
import itertools
import numpy as np

def run(database, port):
    
    client = connect(database, port=port)
    
    actions = ['create', 'read', 'update', 'delete']
    resources = ['patient', 
                 'examination', 
                 'report', 
                 'examination_state', 
                 'report_state']
    
    permission_ = itertools.product(resources, actions)
    Permission.drop_collection()
    permission_list = []
    for it in permission_:
        p = Permission(it[1], it[0])
        p.save()
        permission_list.append(p)    
        
    permission_dict = {'accettazione':np.array([1, 2, 3, 5, 6, 13, 14, 18])-1,
                       'tecnico': np.array([2, 6, 7, 8, 14, 15, 16, 18])-1,
                       'medico': np.array([2, 6, 9, 10, 11, 14, 17, 18, 19])-1,
                       'amministrazione': np.array([2, 6, 10, 14, 18])-1,
                       'admin':np.array([1,2,3,4,5,6,7,8,13,14,15,16,17,18,19,20])-1
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




