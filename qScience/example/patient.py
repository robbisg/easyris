import csv
from mongoengine import connect
from datetime import datetime
from qScience.model.patient import Patient
from qScience.database.base import parse_db_config, easyris_connect
import os


def run(database_config, n_loaded=100):
    
    db_config = parse_db_config(database_config)
    print db_config
    conn = easyris_connect(**db_config)
    database = db_config['database_name']
    db = conn.get_database(database)
    print db.collection_names()

    if 'city' not in db.collection_names():
        # We imported the short version
        # We think that we are testing the app!
        from qScience.example.setup import import_csv
        path = os.path.dirname(os.path.realpath(__file__))
        # Import city
        print os.path.join(path, "files/codicicomuni_test.csv")
        print '------------'
        print '------------'
        print '------------'
        import_csv(database, 
                   'city', 
                   os.path.join(path, "files/codicicomuni_test.csv"))

        
    path = '/'.join(__file__.split('/')[:-1])
    print path
    filepath = os.path.join(path, 'files/db_test_population.csv')
    with open(filepath, 'rb') as csvfile:
        patient_csv = csv.reader(csvfile, delimiter=',')
        for i,row in enumerate(patient_csv):
            if i == 0:
                keys_ = [str.lower(r_) for r_ in row]
            elif i < n_loaded:
                fields_ = dict(zip(keys_, row))
                fields_['birthplace'] = str.upper(fields_['birthplace'])
                fields_['city'] = str.upper(fields_['city'])
                fields_['birthdate'] = datetime.strptime(fields_['birthdate'],
                                                   "%Y-%m-%d" )
                fields_['province'] = None

                patient_ = Patient(**fields_)
                #print fields_

                patient_.save()

