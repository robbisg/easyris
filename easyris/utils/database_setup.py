from mongoengine import connect
import os
import patient_db
import user_db
from easyris.utils import examination_db, report_db


def import_csv(database, collection, filepath):
    
    filename = filepath.split("/")[-1]
    
    print("Importing %s" %(filename))
    command = "mongoimport --db %s \
                           --collection %s \
                           --quiet \
                           --type csv --headerline \
                           --file %s > /dev/null " %(database, collection, filepath)
                           
    os.system(command)


def run(database_config="config/database.cfg", **kwargs):
    
    from easyris.base.database import parse_db_config, easyris_connect
    db_config = parse_db_config(database_config)
    print db_config
    conn = easyris_connect(**db_config)
    db_name = db_config['database_name']
    
    # Always delete database
    if db_name in conn.database_names():
        print "Database found. Deleting it!"
        conn.drop_database(db_name)
    else:
        print "Database not found..."
    
    print " ---- Database population ---"
    path = os.path.dirname(os.path.realpath(__file__))
    # Import city
    import_csv(db_name, 'city', os.path.join(path, "files/codicicomuni2015.csv"))

    print "Import patient.csv"
    if 'n_loaded' in kwargs.keys():
        n_loaded = kwargs['n_loaded']
    else:
        n_loaded = 100
    
    if 'n_patient' in kwargs.keys():
        n_loaded = kwargs['n_patient']
    patient_db.run(database_config, n_loaded=n_loaded)

    # Import priority_db.csv
    import_csv(db_name, 'priority', os.path.join(path, "files/priority_db.csv"))

    # Import nomenclatura_esami.csv
    import_csv(db_name, 'typology', os.path.join(path, "files/nomenclatura_esami.csv"))

    print "Populating users, permissions and roles."
    user_db.run(database_config)
    
    print "Creating dummy examinations."
    if 'n_examination' in kwargs.keys():
        n_loaded = kwargs['n_examination']
    examination_db.run(database_config, n_loaded=n_loaded*2)
    
    print "Creating dummy reports."
    if 'n_report' in kwargs.keys():
        n_loaded = kwargs['n_report']
    report_db.run(database_config, n_loaded=n_loaded)
    
    return

