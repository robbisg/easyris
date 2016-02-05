from mongoengine import *
# from easyris.user.model import User
from easyris.patient.model import Patient


class Priority(Document):
    __collection__ = 'priority'

    priority_name = StringField(required=True)


class PriorityEmbedded(EmbeddedDocument):
    __collection__ = 'priority'

    priority_name = StringField(required=True)


class ExamStatus(Document):
    __collection__ = 'exam_status'

    exam_status_name = StringField(required=True)


class ExamStatusEmbedded(EmbeddedDocument):
    __collection__ = 'exam_status'

    exam_status_name = StringField(required=True)


class Typology(Document):
    __collection__ = 'typology'

    descrizione_ministeriale = StringField(required=True)
    modality = StringField(required=True)
    room = StringField(required=True)
    exam_name = StringField(required=True)
    distretto_corporeo = StringField(required=True)


class TypologyEmbedded(EmbeddedDocument):
    __collection__ = 'typology'

    codice_ministeriale = StringField(required=False)
    codice_regionale = StringField(required=False)
    nota = StringField(required=False)
    descrizione_breve = StringField(required=False)
    descrizione_ministeriale = StringField(required=True)
    tariffa_euro = StringField(required=False)
    annotazioni = StringField(required=False)
    categorie = StringField(required=False)
    modality = StringField(required=True)
    room = StringField(required=True)
    scheduled_station_ae_title = StringField(required=False)
    device_description = StringField(required=False)
    exam_name = StringField(required=True)
    distretto_corporeo = StringField(required=True)


class Examination(Document):
    __collection__ = 'examination'

    id_patient = ReferenceField(Patient)
    medico_richiedente = StringField(required=True)
    data_inserimento = DateTimeField(required=True)

    id_priority = EmbeddedDocumentField(PriorityEmbedded)
    id_exam_status = EmbeddedDocumentField(ExamStatusEmbedded)
    id_typology = EmbeddedDocumentField(TypologyEmbedded)

    # id_creator = ReferenceField(User)
    # id_technician = ReferenceField(User)
    #TODO create Report class and db
    # id_report = StringField(ReferenceField(Report))
    # accession_number = StringField(required=True)
    #TODO per adesso lasciamo il CodiceEsenzione come stringa appena Massimo ci da la tabella dei codici lo convertiamo in id
    # codice_esenzione = StringField(required=True)
    # examination_note = StringField(required=True)
