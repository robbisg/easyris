from mongoengine import *
from pymongo import MongoClient
from codicefiscale import build
from datetime import datetime


class User(object):
    def __init__(self, user, password, role):
        self.user = user
        self.password = password
        self.role = role
        
    def has_permission(self, action, resource):
        permissions = self.role.get_permissions()
        for p in permissions:
            if p.action == action and p.resource == resource:
                return True
        return False
        

class Role(object):
    def __init__(self, name):
        self.name = name
        self.permission = []
        
    def add_permission(self, permission):
        self.permission.append(permission)
        
    def get_permissions(self):
        return self.permission
        

class Permission(object):
    def __init__(self, action, resource):
        
        self.action = action
        self.resource = resource