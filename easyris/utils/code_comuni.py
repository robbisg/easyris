from mongoalchemy.session import Session
from mongoalchemy.document import Document, Index
from mongoalchemy.fields import StringField
from codicefiscale import build


class CF_codici_comuni(Document):
    config_collection_name = 'patients'

    # Setting the possible values by using fields
    codice = StringField(required=True)
    Prov = StringField(required=True)
    Denom_Italiana = StringField(required=True)
