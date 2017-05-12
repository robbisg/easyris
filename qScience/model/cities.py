from mongoengine import *
from codicefiscale import build
from qScience.base import QScienceQuerySet, QScienceMixin


class City(QScienceMixin, Document):
    __collection__ = 'cf_codici_comuni'
    meta = {'queryset_class': QScienceQuerySet}
    # Setting the possible values by using fields
    Codice = StringField(required=True)
    Prov = StringField(required=True)
    Denom_Italiana = StringField(required=True)
