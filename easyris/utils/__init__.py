from datetime import datetime
import numpy as np


def parse_date(date):
    
    try:
        seconds_ = np.int(date)/1000.
        date_ = datetime.fromtimestamp(seconds_)
    except ValueError, err:
        date_ = datetime.strptime(date, 
                                  "%Y-%m-%dT%H:%M:%S.%fZ" )
        
    return date_