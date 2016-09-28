from mongoengine import *
from codicefiscale import build
from easyris.base import EasyRisQuerySet, EasyRisDocument


class City(EasyRisDocument):
    __collection__ = 'cf_codici_comuni'
    meta = {'queryset_class': EasyRisQuerySet}
    # Setting the possible values by using fields
    Codice = StringField(required=True)
    Prov = StringField(required=True)
    Denom_Italiana = StringField(required=True)
