from mongoengine import Document, StringField, ReferenceField, \
                    ListField, BooleanField
from mongoengine.queryset import QuerySet
from mongoengine.dereference import DeReference
from pymongo import MongoClient
from datetime import datetime
from passlib.hash import sha256_crypt
from flask_login import UserMixin
import itertools
from easyris.base import EasyRisDocument, EasyRisQuerySet


class UserEasyrisQuerySet(QuerySet):
    """
    This is specifically used to avoid the inclusion
    of password in the message sent to the frontend
    """
    def as_pymongo(self):
        fields = User._fields.keys()
        fields.remove('password')
        return [e._to_easyris(fields=fields) for e in self.all()]


class Permission(Document):
    
    __collection__ = 'permission'
    
    action = StringField(required=True)
    resource = StringField(required=True)
    
    

class Role(Document):
    
    __collection__ = 'role'
    
    role_name = StringField(required=True, unique=True)
    permissions = ListField(ReferenceField(Permission))
    
        
    def add_permission(self, permission):
        self.permissions.append(permission)
        
    def get_permissions(self):
        return self.permissions



class User(EasyRisDocument, UserMixin):
    
    meta = {'queryset_class': UserEasyrisQuerySet}
    
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
    
    
    def has_role(self, rolename):
        for role in self.roles:
            if role.role_name == rolename:
                return True
        
        return False
        
       
    def _get_subfields(self, document):
                
        fields_ = {
                   'role': ['role_name']
                   }
        
        dereference = DeReference()
        document = dereference(document)
        
        return [d.to_mongo(fields=fields_[d.__collection__]) for d in document]
        
        #return document.to_mongo(fields=fields_[document.__collection__])
    
