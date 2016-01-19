from mongoengine import connect
import os
import patient_db


def run():
    conn = connect('easyris')
    conn_check = str(conn.database_names()[0])
    
    if conn_check == 'easyris' :
        print "Database found. Deleting it!"
        conn.drop_database("easyris")
    else:
        print "Database not found..."
    
    
    print " ---- Database population ---"
    print "Import codicicomuni2015.csv"
    os.system("mongoimport --db easyris \
                           --collection CF_codici_comuni \
                           --type csv --headerline \
                           --file /var/www/backend/easyris/utils/files/codicicomuni2015.csv")
    print "Import patient.csv"
    patient_db.main()