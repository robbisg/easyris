#!/usr/bin/env python
import csv
from mongoengine import connect
from datetime import datetime
from easyris.patient.model import Patient
import os

def main(n_loaded=100):
    connect('easyris', port=27017)
    #Patient.drop_collection()
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

if __name__ == '__main__':
    main()
