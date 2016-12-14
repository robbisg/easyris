import logging
import logging.handlers


def enable_logging():

    logger = logging.getLogger('easyris_logger')
    logger.setLevel(logging.INFO)
    # create file handler which logs even debug messages
    fh = logging.handlers.RotatingFileHandler('/home/vagrant/easyris.log',
                                              maxBytes=2*1024*1024,
                                              backupCount=5)
    fh.setLevel(logging.INFO)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('----------\n'+
                                  '%(asctime)s - '+
                                  '%(levelname)s - '+ 
                                  '[%(pathname)s:'+
                                  '%(lineno)s] - '+
                                  '%(name)s - :\n'+
                                  '%(message)s')
    
    
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    
    return fh


def store_event():
    
    return