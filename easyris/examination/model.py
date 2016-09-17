from mongoengine import Document, StringField, ReferenceField, DateTimeField, EmbeddedDocumentField
from bson.son import SON
from mongoengine.base.common import get_document, ALLOW_INHERITANCE
from mongoengine.queryset import QuerySet
from mongoengine import signals
from mongoengine.common import _import_class
from easyris.user.model import User
from easyris.patient.model import Patient
from easyris.examination.status import NewExaminationStatus, ExaminationStatus
from easyris.base import EasyRisDocument, EasyRisQuerySet




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


class Examination(EasyRisDocument):
    
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
    
    
    def set_accession_number(self):
        # TODO: Accession number must depend on
        # device, date, patient and body part
        # TODO: Query su Examination per vedere se ci sono esami con
        # device, data, pazienti e body part uguali e mettere lo stesso num.
        return
    
    
    
    def _get_subfields(self, document):
                
        fields_ = {
                   'patient': ['first_name', 'last_name', 'id_patient'],
                   'typology': ['examination_name', 'room', 'distretto_corporeo'],
                   'priority': ['priority_name'],
                   'user':['username']
                   }
        
        return document.to_mongo(fields=fields_[document.__collection__])
    
    
            

class ExaminationTemplate(EasyRisDocument):
    
    id_examination = ReferenceField(Examination)
    template = StringField()
    
    
            