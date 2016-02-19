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
                           --file easyris/utils/files/codicicomuni2015.csv")
    print "Import patient.csv"
    patient_db.main()

    print "Import priority_db.csv"
    os.system("mongoimport --db easyris \
                           --collection priority \
                           --type csv --headerline \
                           --file easyris/utils/files/priority_db.csv")

    print "Import exam_status_db.csv"
    os.system("mongoimport --db easyris \
                           --collection exam_status \
                           --type csv --headerline \
                           --file easyris/utils/files/exam_status_db.csv")

    print "Import nomenclatura_esami.csv"
    os.system("mongoimport --db easyris \
                           --collection typology \
                           --type csv --headerline \
                           --file easyris/utils/files/nomenclatura_esami.csv")

    print "Import permission.csv"
    os.system("mongoimport --db easyris \
                           --collection permission \
                           --type csv --headerline \
                           --file easyris/utils/files/permission.csv")

    print "Import role.csv"
    os.system("mongoimport --db easyris \
                           --collection role \
                           --type csv --headerline \
                           --file easyris/utils/files/role.csv")

    print "Import username.csv"
    os.system("mongoimport --db easyris \
                           --collection username \
                           --type csv --headerline \
                           --file easyris/utils/files/username.csv")

    print "Import report_status.csv"
    os.system("mongoimport --db easyris \
                           --collection report_status \
                           --type csv --headerline \
                           --file easyris/utils/files/report_status.csv")

    print "Import report.csv"
    os.system("mongoimport --db easyris \
                           --collection report \
                           --type csv --headerline \
                           --file easyris/utils/files/report.csv")
