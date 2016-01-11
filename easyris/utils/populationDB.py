from mongoengine import connect
import os
import patient_db

conn = connect('easyris')
conn_check = str(conn.database_names()[0])

if conn_check == 'easyris' :
    print "ok easyris exists. Now drop it "
    conn.drop_database(conn_check)
else:
    print "DB not. Now i create it."

print "Import codicicomuni2015.csv"
os.system("mongoimport --db easyris --collection CF_codici_comuni --type csv --headerline --file /var/www/backend/easyris/utils/files/codicicomuni2015.csv")
print "Import patient.csv"
patient_db.main()