from mongoengine import *
from pymongo import MongoClient
from datetime import datetime
from passlib.hash import sha256_crypt
from flask_login import UserMixin
import itertools


class Permission(Document):
    
    action = StringField(required=True)
    resource = StringField(required=True)
    
    

class Role(Document):
    
    role_name = StringField(required=True, unique=True)
    permissions = ListField(ReferenceField(Permission))
    
        
    def add_permission(self, permission):
        self.permissions.append(permission)
        
    def get_permissions(self):
        return self.permissions



class User(Document, UserMixin):
    
    __collection__ = 'user'
    
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    
    roles = ListField(ReferenceField(Role))
    
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    
    # TODO: Check email formatting (frontend?)
    email = StringField(required=True)
    telephone_number = StringField(required=True)
    mobile_number = StringField(required=True)
    
    active = BooleanField(default=True)
    
    
    def clean(self):
        
        self.password = sha256_crypt.encrypt(self.password)
    
    
    def has_permission(self, action, resource):
        permissions = [role.get_permissions() for role in self.roles]
        permissions = list(itertools.chain(*permissions))
        # print permissions
        for p in permissions:
            if p.action == action and p.resource == resource:
                return True
        return False
           
    def check_password(self, password):

        if sha256_crypt.verify(password, self.password):
            return True
        return False 
      
    def get_id(self):
        return unicode(self.id)