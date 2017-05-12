import logging
import logging.handlers
import os


class EasyRisFormatter(logging.Formatter):
    def format(self, record):
        if record.pathname != None:
            # truncate the pathname
            path_split = record.pathname.split("/")
            begin = [i for i, p in enumerate(path_split) if p == "qScience"]
            record.pathname = "/".join(path_split[begin[0]:])
        return super(EasyRisFormatter, self).format(record)



def enable_logging():

    logger = logging.getLogger('easyris_logger')
    logger.setLevel(logging.DEBUG)
    
    # create file handler which logs even debug messages
    fh = logging.handlers.RotatingFileHandler('/home/vagrant/easyris.log',
                                              maxBytes=2*1024*1024,
                                              backupCount=5)
    fh.setLevel(logging.DEBUG)
    
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # create formatter and add it to the handlers
    format_ = "%(asctime)s: %(levelname)s [%(pathname)s:%(lineno)s %(funcName)s()] | %(message)s"
    
    formatter = EasyRisFormatter(format_)
        
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)
    
    return fh
