from mongoengine import Document, StringField, ReferenceField, DateTimeField, EmbeddedDocumentField
from bson.son import SON
from mongoengine.base.common import get_document, ALLOW_INHERITANCE
from mongoengine.queryset import QuerySet
from mongoengine import signals
from mongoengine.common import _import_class
from easyris.user.model import User
from easyris.patient.model import Patient
from easyris.examination.status import NewExaminationStatus, ExaminationStatus
from easyris.base import EasyRisMixin, EasyRisQuerySet
from numpy.random.mtrand import randint


import logging
logger = logging.getLogger("easyris_logger")

class Priority(Document):
    __collection__ = 'priority'

    priority_name = StringField(required=True)



class Typology(Document):
    # Tabella di esami ministeriali
    __collection__ = 'typology'

    codice_ministeriale = StringField(required=False)
    codice_regionale = StringField(required=False)
    nota = StringField(required=False)
    descrizione_breve = StringField(required=False)
    descrizione_ministeriale = StringField(required=True)
    tariffa_euro = StringField(required=False)
    annotazioni = StringField(required=False)
    categorie = StringField(required=False)
    modality = StringField(required=True) # MR, TAC, ECO
    room = StringField(required=True) # Stanza fisica dove sta il device
    scheduled_station_ae_title = StringField(required=False) # Campo PACS
    device_description = StringField(required=False) # Descrizione scanner/device
    examination_name = StringField(required=True)
    distretto_corporeo = StringField(required=True) # Testa/collo baby one two three


class Examination(EasyRisMixin, Document):
    
    meta = {'queryset_class': EasyRisQuerySet}
    
    __collection__ = 'examination'

    id_patient = ReferenceField(Patient, required=True)
    medico_richiedente = StringField(required=True)
    data_inserimento = DateTimeField(required=True)
    
    id_priority = ReferenceField(Priority, required=True)

    status = EmbeddedDocumentField(ExaminationStatus, default=NewExaminationStatus())
    status_name = StringField(required=True, default='new')
    id_typology = ReferenceField(Typology, required=True)
    
    # TODO: Check role?
    id_creator = ReferenceField(User, required=True)
    id_technician = ReferenceField(User)
        
    # Accession number raggruppa esami che vanno fatti insieme
    accession_number = StringField(required=True)
    # TODO:per adesso lasciamo il CodiceEsenzione 
    # come stringa appena Massimo ci da la tabella 
    # dei codici lo convertiamo in id
    codice_esenzione = StringField()
    examination_note = StringField()
    
    
    def clean(self):
        self.accession_number = self.set_accession_number(date=self.data_inserimento,
                                                          patient=self.id_patient,
                                                          room=self.id_typology.room,
                                                          body_part=self.id_typology.distretto_corporeo)
    
    
    
    def set_accession_number(self, date, patient, room, body_part):

        klass = self.__class__
        current_patient_ex = klass.objects(id_patient=self.id_patient.id)
        if len(current_patient_ex) == 0:
            return self._get_accession_number(date)
        
        today_examinations = current_patient_ex.filter(data_inserimento=date)
        if len(today_examinations) == 0:
            return self._get_accession_number(date)
        
        typology = Typology.objects(room=room,
                                    distretto_corporeo=body_part)
        
        for t in typology:
            typology_examination = today_examinations.filter(id_typology=t.id)
            if len(typology_examination) > 0:
                logger.debug(typology_examination[0].accession_number)
                return typology_examination[0].accession_number
            
        return self._get_accession_number(date)
    
    
    def _get_accession_number(self, date):
        import numpy as np
        now_ = str(date)
        year = str(now_).split('-')[0]
        month = str(now_).split('-')[1]
        day = str(now_)[8:10]
        random_num = str(np.random.randint(1000000, 1999999))[1:]
        return year+month+day+random_num
    
    
    
    def _get_subfields(self, document):
                
        fields_ = {
                   'patient': ['first_name', 'last_name', 'id_patient'],
                   'typology': ['examination_name', 
                                'room', 
                                'distretto_corporeo'],
                   'priority': ['priority_name'],
                   'user':['username']
                   }
        
        return document.to_mongo(fields=fields_[document.__collection__])
    
    
class ExaminationTemplate(EasyRisMixin, Document):
    """
    This should be used only for report template
    """
    
    id_examination = ReferenceField(Examination)
    template = StringField()
    
    
            