from datetime import datetime
import numpy as np


def parse_date(date):
    
    try:
        seconds_ = np.int(date)/1000.
        date_ = datetime.fromtimestamp(seconds_)
    except ValueError, _:
        date_ = datetime.strptime(date, 
                                  "%Y-%m-%dT%H:%M:%S.%fZ" )
        
    return datetime(year=date_.year, day=date_.day, month=date_.month)


def date_from_json(date):
    
    try:
        mongo_date = datetime.strptime(date, "%d/%m/%Y")
    except ValueError, _:
        mongo_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ" )
        
    return mongo_date.replace(hour=0, minute=0, second=0)