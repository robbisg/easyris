from mongoengine import *
from codicefiscale import build


class CF_codici_comuni(Document):
    __collection__ = 'cf_codici_comuni'

    # Setting the possible values by using fields
    codice = StringField(required=True)
    Prov = StringField(required=True)
    Denom_Italiana = StringField(required=True)
