from easyris import create_app
from easyris.log import enable_logging
import click
import os

'''
@click.command()
@click.option('--config', default='config/easyris.cfg', help='Configuration file of flask (default=config/easryis.cfg)')
@click.option('--database_name', default='easyris', help='The database name to be used. (default=easyris)')
@click.option('--database_port', default=27017, help='The port with the database service (default=27017)')
@click.option('--permanent_session_lifetime', default=24, help='Duration time of the session (default=24 (hours))')
'''
def init_app(**kwargs):
    
    #config = kwargs.pop('config')

    app = create_app()
    return app
    

if __name__ == '__main__':
    
    app = init_app()
    
    handler = enable_logging()
    app.logger.addHandler(handler)
    
    ssl_path = app.config['SSL_PATH']
    
    app.run(host='0.0.0.0', 
            port=5000, 
            debug=True,
            threaded=True,
            ssl_context=(os.path.join(ssl_path, "webserver.crt"),
                         os.path.join(ssl_path, "webserver.key")
                         )
          )
    
    app.toolbar.init_app(app)