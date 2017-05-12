from mongoengine import Document, StringField, ReferenceField, DateTimeField, EmbeddedDocumentField
from bson.son import SON
from mongoengine.base.common import get_document
from mongoengine.queryset import QuerySet
from mongoengine import signals
from mongoengine.common import _import_class
from mongoengine.fields import ListField
from mongoengine.base import BaseDocument
import os
import logging
logger = logging.getLogger("easyris_logger")


class QScienceQuerySet(QuerySet):

    def as_pymongo(self):
        
        return [e._to_easyris() for e in self.all()]



class QScienceMixin(object):
    
    meta = {
        'abstract': True,
    }
    
    def _get_subfields(self, document, fields=dict()):
        """
        This should always be overrided to get fields 
        from the document passed
        """
        return
    
    
    
    def _to_easyris(self, use_db_field=True, fields=None):
        """
        Return as SON data ready for use with MongoDB.
        """
        if not fields:
            fields = []
#             
#         logger.critical(self.__collection__)
#         logger.critical(fields)
        data = SON()
        data["_id"] = None
        data['_cls'] = self._class_name
        EmbeddedDocumentField = _import_class("EmbeddedDocumentField")
        ListField = _import_class("ListField")
        ReferenceField = _import_class("ReferenceField")
        Document = _import_class("Document")
        # only root fields ['test1.a', 'test2'] => ['test1', 'test2']
        root_fields = set([f.split('.')[0] for f in fields])
    
        for field_name in self:
            
            if root_fields and field_name not in root_fields:
                continue

            value = self._data.get(field_name, None)
            field = self._fields.get(field_name)
            
#             logger.critical('----')
#             logger.critical("value: "+str(value))
#             logger.critical("field: "+str(field))
#             logger.critical("field_name: "+str(field_name))
            
            if field is None and self._dynamic:
                field = self._dynamic_fields.get(field_name)
    
            if value is not None:
    
                if fields:
                    key = '%s.' % field_name
                    embedded_fields = [
                        i.replace(key, '') for i in fields
                        if i.startswith(key)]
    
                else:
                    embedded_fields = []
                
                
                if isinstance(field, ReferenceField):
                    value = self._get_subfields(self[field_name])
                    
                elif isinstance(field, ListField):
                    
                    value = self._get_subfields(value)
                else:
                    
                    value = field.to_mongo(value, 
                                           #use_db_field=use_db_field,
                                           #fields=embedded_fields
                                           )
    
            # Handle self generating fields
            if value is None and field._auto_gen:
                value = field.generate()
                self._data[field_name] = value
    
            if value is not None:
                if use_db_field:
                    data[field.db_field] = value
                else:
                    data[field.name] = value
    
        # If "_id" has not been set, then try and set it
        
        if isinstance(self, Document):
            if data["_id"] is None:
                data["_id"] = self._data.get("id", None)
    
        if data['_id'] is None:
            data.pop('_id')
    
        # Only add _cls if allow_inheritance is True
        if (not hasattr(self, '_meta') or
                not self._meta.get('allow_inheritance', False)):
            data.pop('_cls')
    
        return data
    
    
    
def parse_db_config(config_filename):
    
    import ConfigParser
    import sys
    
    config = ConfigParser.ConfigParser()
    config.read(os.path.join(sys.path[0], config_filename))
    
    print os.path.join(sys.path[0], config_filename)
    
    db_config = dict(config.items('mongodb'))
    
    nodes = db_config.pop('database_config').split(',')
    
    host_string = []
    for node in nodes:
        node_string = "%s:%s" % (config.get(node, 'database_ip') ,
                                 config.get(node, 'database_port'))
        host_string.append(node_string)
    host_string = ','.join(host_string)
    #host_string = "mongodb://%s" % (host_string)
    
    db_config['host'] = host_string
    
    
    if 'database_rs' in db_config:
        from pymongo import ReadPreference
        db_config['read_preference'] = ReadPreference.PRIMARY_PREFERRED
        db_config['replicaSet'] = db_config.pop('database_rs')
               
    return db_config


def easyris_connect(database_name='qScience', 
                     host='localhost:27017', 
                     **kwargs):
        
    from mongoengine import connect
    # read_preference=ReadPreference.SECONDARY_PREFERRED
    host = 'mongodb://'+host
    
    client = connect(database_name, 
                     host=host, 
                     **kwargs)
        
    return client


def restore_db(db_filename):
    db_config = parse_db_config(db_filename)
    db_name = db_config['database_name']
    command = "mongorestore --quiet -d %s %s" % (db_name, 'qScience/example/easyris_mock')
    print command
    os.system(command)
    
    
    
    
    