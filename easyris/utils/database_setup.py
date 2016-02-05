from mongoengine import connect
import os
import patient_db


def run():
    conn = connect('easyris')
    conn_check = str(conn.database_names()[0])
    
    if conn_check == 'easyris':
        print "Database found. Deleting it!"
        conn.drop_database("easyris")
    else:
        print "Database not found..."

    print " ---- Database population ---"
    print "Import codicicomuni2015.csv"
    os.system("mongoimport --db easyris \
                           --collection city \
                           --type csv --headerline \
                           --file /var/www/backend/easyris/utils/files/codicicomuni2015.csv")
    print "Import patient.csv"
    patient_db.main()

    print "Import priority_db.csv"
    os.system("mongoimport --db easyris \
                           --collection priority \
                           --type csv --headerline \
                           --file /var/www/backend/easyris/utils/files/priority_db.csv")

    print "Import exam_status_db.csv"
    os.system("mongoimport --db easyris \
                           --collection exam_status \
                           --type csv --headerline \
                           --file /var/www/backend/easyris/utils/files/exam_status_db.csv")

    print "Import nomenclatura_esami.csv"
    os.system("mongoimport --db easyris \
                           --collection typology \
                           --type csv --headerline \
                           --file /var/www/backend/easyris/utils/files/nomenclatura_esami.csv")

