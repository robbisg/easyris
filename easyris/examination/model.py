from mongoengine import Document, StringField, ReferenceField, DateTimeField
from easyris.user.model import User
from easyris.patient.model import Patient
from easyris.examination.status import NewExaminationStatus


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


class Examination(Document):
    __collection__ = 'examination'

    id_patient = ReferenceField(Patient)
    medico_richiedente = StringField(required=True)
    data_inserimento = DateTimeField(required=True)

    id_priority = ReferenceField(Priority)
    
    status_name = StringField(required=True, default='NEW')
    id_typology = ReferenceField(Typology)
    
    # TODO: Check role?
    id_creator = ReferenceField(User)
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
    
        