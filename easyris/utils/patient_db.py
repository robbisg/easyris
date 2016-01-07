import csv
from mongoengine import connect
from datetime import datetime
from easyris.patient.model import Patient

def main():
    #connect('easyris', port=27017)
    #Patient.drop_collection()
    
    with open('/vagrant/easyris/easyris/utils/files/db_test_population.csv', 'rb') as csvfile:
        patient_csv = csv.reader(csvfile, delimiter=',')
        for i,row in enumerate(patient_csv):
            if i == 0:
                keys_ = [str.lower(r_) for r_ in row]
            elif i<5:
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