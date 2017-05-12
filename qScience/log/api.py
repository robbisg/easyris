from flask import Blueprint, request
from flask_cors.decorator import cross_origin
from qScience.utils.decorators import jsonp
from qScience.message.base import message_to_http
import json

from qScience.message.base.base import MessageHeader, Message


event = Blueprint('event', __name__)

import logging
logger = logging.getLogger("easyris_logger")

@event.route('/', methods=['POST', 'OPTIONS'])
@jsonp
@cross_origin(origin=None,
              methods=['GET', 'POST', 'OPTIONS'],
              allow_headers=['X-Requested-With',
                             'Content-Type',
                             'Origin'],
              supports_credentials=True)
def post_event():
    
    if request.method == 'POST':
        
        logger.debug(str(request))
        logger.debug(request.headers)
        logger.debug(request.user_agent)
        logger.debug(request.remote_addr)
        logger.debug(request.referrer)
        query = json.loads(request.data)
        query['ip'] = request.remote_addr
        query['user_agent'] = str(request.user_agent)
        logger.debug(query)
        #save_event.delay(query)
        
        response = message_to_http(Message(MessageHeader(600, 
                                                         "Event sent to database", 
                                                         "system")
                                           )
                                   )
        logger.debug(response)
        
        return response
    
    
    
    